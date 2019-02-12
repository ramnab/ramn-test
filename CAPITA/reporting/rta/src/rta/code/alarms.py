from datetime import datetime
from datetime import timedelta
import boto3
import logging
import json
from botocore.exceptions import ClientError
import os


logger = logging.getLogger()
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)


class Alarm:

    BREAK_CODES = ["Break", "Lunch"]
    EXCEPTION_CODES = ['System Down', 'Admin', 'Training', '121']

    def __init__(self, alarmcode, event_types, schedules):
        self.alarmcode = alarmcode
        self.event_types = event_types
        self.schedules = schedules

    def filter(self, events):
        return [event for event in events
                if event.get("EventType") in self.event_types]

    def get_ts(self, ts):
        try:
            ts1 = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')
        except Exception:
            ts1 = datetime.strptime(ts, '%Y-%m-%dT%H:%M')
        return ts1

    def is_between(self, w, event):
        if not event:
            return False

        t1 = self.get_ts(w.get("T1"))
        t2 = self.get_ts(w.get("T2"))
        event_ts = self.get_ts(event.get("EventTimestamp"))
        result = t1 < event_ts < t2
        # print(f"is_between: {t1} < {event_ts} < {t2} = {result}")
        return result

    def after(self, ts, event):
        if not event:
            return False
        t = self.get_ts(ts)
        event_ts = self.get_ts(event.get("EventTimestamp"))
        result = event_ts > t
        logger.debug(f"{self.alarmcode}: {str(event_ts)}"
                     f" > {str(t)} = {result}")
        return result

    def before(self, ts, event):
        if not event:
            return False
        event_ts = self.get_ts(event.get("EventTimestamp"))
        t = self.get_ts(ts)
        result = event_ts < t
        logger.debug(f"{self.alarmcode}: {str(event.get('EventTimestamp'))}"
                     f" < {str(t)} = {result}")

        return result

    def set_alarm(self, username, ts, display_ts, extra,
                  trigger, reason, ttl=None):
        logger.info(f"Setting alarm {self.alarmcode} for {username}"
                    f" at {ts} with TTL {ttl}: {display_ts} "
                    f" extra: {str(extra)}"
                    f" reason: {reason}")
        if not ttl:
            ttl = self.get_ts(ts) + timedelta(hours=12)
        else:
            ttl = self.get_ts(ttl)

        firstname = trigger.get("CurrentAgentSnapshot", {}) \
                           .get("Configuration", {}) \
                           .get("FirstName", "-")

        lastname = trigger.get("CurrentAgentSnapshot", {}) \
                          .get("Configuration", {}) \
                          .get("LastName", "-")

        item = {
            "username": username,
            "alarmcode": self.alarmcode,
            "ts": ts,
            "firstname": firstname,
            "lastname": lastname,
            "display_ts": display_ts,
            "extra": extra,
            "event": trigger,
            "reason": reason,
            "ttl": int(ttl.timestamp()),
            "httl": str(ttl)
        }
        logger.debug(f"Adding to db: {json.dumps(item, indent=2)}")
        if self.table:
            response = self.table.put_item(Item=item)
            logger.debug(f"Put item reponse = {response}")
        else:
            logger.error("Dynamo db table not set!")

    def clear_alarm(self, username):
        logger.info(f"Clearing alarm {self.alarmcode} for {username}")
        if self.table:
            try:
                key = {"username": username, "alarmcode": self.alarmcode}
                response = self.table.delete_item(Key=key)
                logger.debug(response)
            except ClientError as e:
                logger.error(e)
                raise Exception("Dynamodb exception for delete_item")
        else:
            logger.error("Dynamo db table not set!")

    def update_display_ts(self, username, display_ts):
        logger.info(f"Updating alarm {self.alarmcode} display ts "
                    f"for user {username} to {display_ts}")
        if self.table:
            try:
                response = self.table.update_item(
                    Key={"username": username, "alarmcode": self.alarmcode},
                    UpdateExpression="set display_ts = :d",
                    ExpressionAttributeValues={
                        ':d': display_ts
                    }
                )
                logger.debug(f"Update DB response: {json.dumps(response)}")
            except ClientError as e:
                logger.error(e)
                raise Exception("Dynamodb exception for delete_item")
        else:
            logger.error("Dynamo db table not set!")

    def typed_event(self, typ, events):
        for event in events:
            if event.get("EventType") == typ:
                return event
        return None

    def agent_state(self, event):
        return event.get("CurrentAgentSnapshot", {}) \
                    .get("AgentStatus", {}) \
                    .get("Name")

    def get_alarm_times(self, username, asList=False):
        alarms = self.schedules.get(username).get('ALARMS')
        if not alarms.get(self.alarmcode):
            logger.debug(f"No alarm params exist for user {username}")
            return {}
        if asList:
            return alarms.get(self.alarmcode)
        else:
            return alarms.get(self.alarmcode)[0]

    def time_diff_mins(self, t1, t2):

        ts1 = self.get_ts(t1)
        ts2 = self.get_ts(t2)

        if ts1 and ts2:
            diff = ts1 - ts2
            return abs(int(divmod(diff.total_seconds(), 60)[0]))
        else:
            raise Exception(f"Time parse exception in time_diff_mins with "
                            f"t1={t1} and t2={t2}")

    def get_schedule(self, username, code="SHIFT"):
        return self.schedules.get(username).get('SCHEDULE').get(code)

    def set_table(self, table):
        self.table = table

    def mins_pp(self, mins):
        (hours, minutes) = divmod(mins, 60)
        return f"{hours:02d}:{minutes:02d}"

    def pp_date(self, date):
        d = self.get_ts(date)
        return datetime.strftime(d, '%H:%M:%S %d/%m/%Y')


class BSE(Alarm):
    '''
    Begin Shift Early
    Alarm is set when agent signs in between
        shift start time - window and shift start time - grace

    Alarm is cleared when agent heart beat / login event after
        shift start time - grace

    '''

    def __init__(self, schedules):
        super().__init__("BSE", ["LOGIN", "HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if state:
                '''Clear alarm conditions'''
                event = self.typed_event("HEART_BEAT", filtered_events)
                if state.get("end"):
                    if self.after(state.get("end"), event):
                        self.clear_alarm(username)

            if not state:
                '''Set alarm conditions'''
                event = self.typed_event("LOGIN", filtered_events)
                if event:
                    windows = self.get_alarm_times(username, True)
                    for window in windows:
                        print(f"window: {str(window)}")
                        if self.is_between(window, event):
                            ts = event.get("EventTimestamp")
                            ts_pp = datetime.strftime(self.get_ts(ts),
                                                      '%H:%M:%S %d/%m/%Y')
                            shift_start = window.get("start")
                            time_diff = self.time_diff_mins(shift_start, ts)
                            display_ts = self.mins_pp(time_diff)
                            ttl = window.get("T2")
                            reason = (f"{username} login at {ts_pp} "
                                      f"before shift start at "
                                      f"{self.pp_date(shift_start)}")
                            self.set_alarm(username, ts, display_ts,
                                           {"end": window.get("T2")},
                                           event, reason, ttl)
                            break


class BSL(Alarm):
    '''
    Begin Shift Late

    Alarm is set when agent has state 'Offline' between
        shift start time + grace and shift end time

    Alarm cleared on agent login or end of shift
    '''

    def __init__(self, schedules):
        super().__init__("BSL", ["LOGIN", "HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if state:
                '''Incremental display ts'''
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    event_ts = event.get("EventTimestamp")
                    shift_start = self.shift_start(username)
                    time_diff = self.time_diff_mins(shift_start, event_ts)
                    display_ts = self.mins_pp(time_diff)
                    self.update_display_ts(username, display_ts)

                '''Clear alarm conditions'''
                event = self.typed_event("LOGIN", filtered_events)
                if event:
                    self.clear_alarm(username)
                t2 = state.get("end")
                if t2 and self.after(t2, event):
                    self.clear_alarm(username)

            if not state:
                '''Set alarm conditions'''
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    agent_status = self.agent_state(event)
                    if agent_status == "Offline":
                        windows = self.get_alarm_times(username, True)
                        for window in windows:
                            if self.is_between(window, event):
                                ts = event.get("EventTimestamp")
                                ts_pp = self.pp_date(ts)
                                shift_start = window.get("start")
                                time_diff = self.time_diff_mins(shift_start, ts)
                                display_ts = self.mins_pp(time_diff)
                                reason = (f"{username} login at {ts_pp} "
                                          f"after shift start at "
                                          f"{self.pp_date(shift_start)}")

                                self.set_alarm(username, ts, display_ts,
                                               {"end": window.get('end')},
                                               event, reason)
                                break


class ESE(Alarm):
    '''
    End Shift Early
    Alarm is set when agent signs out before
        shift end time - grace (T1)

    Reported time is shift end time

    Alarm is cleared by TTL after
        shift end time - grace (T1)
    '''

    def __init__(self, schedules):
        super().__init__("ESE", ["LOGOUT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if not state:
                '''Set alarm conditions'''
                event = self.typed_event("LOGOUT", filtered_events)
                if event:
                    windows = self.get_alarm_times(username, True)
                    for window in windows:
                        if self.is_between(window, event):
                            # the reported time shift end time
                            ts = event.get("EventTimestamp")
                            ts_pp = self.pp_date(ts)
                            shift_end = window.get("end")
                            time_diff = self.time_diff_mins(ts, shift_end)
                            display_ts = self.mins_pp(time_diff)
                            ttl = window.get("T1")
                            reason = (f"{username} logged out at {ts_pp} "
                                      f"before shift end at "
                                      f"{self.pp_date(shift_end)}")
                            self.set_alarm(username, ts, display_ts, {},
                                           event, reason, ttl)


class ESL(Alarm):
    '''
    End Shift Late
    Alarm is set when agent is still logged in between
        shift end time + grace (T1) and shift end time + window (T2)

    Reported time is event timestamp

    Alarm is cleared by TTL after
        shift end time + window
    or if agent goes Offline
    '''

    def __init__(self, schedules):
        super().__init__("ESL", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:

            if state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                '''Incremental display ts'''
                if event and self.agent_state(event) != "Offline":
                    ts = event.get("EventTimestamp")
                    shift_end = self.shift_end(username)
                    time_diff = self.time_diff_mins(shift_end, ts)
                    display_ts = self.mins_pp(time_diff)
                    self.update_display_ts(username, display_ts)

                '''Clear alarm conditions'''
                if event and self.agent_state(event) == "Offline":
                    self.clear_alarm(username)

            if not state:
                '''Set alarm conditions'''
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    if self.agent_state(event) != "Offline":
                        windows = self.get_alarm_times(username, True)
                        for window in windows:
                            if self.is_between(window, event):
                                # the reported time shift end time
                                ts = event.get("EventTimestamp")
                                ts_pp = self.pp_date(ts)
                                shift_end = window.get("end")
                                time_diff = self.time_diff_mins(shift_end, ts)
                                display_ts = self.mins_pp(time_diff)
                                ttl = window.get("T2")
                                reason = (f"{username} not offline at {ts_pp} "
                                          f"after end of shift at "
                                          f"{self.pp_date(shift_end)}")
                                self.set_alarm(username, ts, display_ts, {},
                                               event, reason, ttl)
                                break


class BBE(Alarm):
    '''
    Begin Break Early
    Alarm is set when an agent enters state of
    'Break' or 'Lunch'
    between
        break start time - window (T1) and break start time - grace (T2)

    '''

    def __init__(self, schedules):
        super().__init__("BBE", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    bbes = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)
                    for bbe in bbes:
                        if self.is_between(bbe, event) \
                           and agent_state in self.BREAK_CODES:
                            ts = event.get("EventTimestamp")
                            ts_pp = self.pp_date(ts)
                            break_start = bbe.get("start")
                            time_diff = self.time_diff_mins(break_start, ts)
                            display_ts = self.mins_pp(time_diff)
                            ttl = bbe.get("T2")
                            reason = (f"{username} entered break at {ts_pp} "
                                      f"earlier than expected start "
                                      f"time of "
                                      f"{self.pp_date(break_start)}")
                            self.set_alarm(username, ts, display_ts, {},
                                           event, reason, ttl)
                            break


class EBL(Alarm):
    '''
    End Break Late
    Alarm is set when an agent is a status of break between
        break end time + grace (T1) and break end time + window (T2)

    Alarm cleared at break end + window (T2)
    '''

    def __init__(self, schedules):
        super().__init__("EBL", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                break_start1 = state.get("extra", {}).get("start")
                agent_state = self.agent_state(event)
                if event and break_start1 and agent_state in self.BREAK_CODES:
                    event_ts = event.get("EventTimestamp")
                    time_diff = self.time_diff_mins(break_start1, event_ts)
                    display_ts = self.mins_pp(time_diff)
                    self.update_display_ts(username, display_ts)

            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    ebls = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)
                    for ebl in ebls:
                        if self.is_between(ebl, event) and \
                           agent_state in self.BREAK_CODES:
                            ts = event.get("EventTimestamp")
                            ts_pp = self.pp_date(ts)
                            ttl = ebl.get("T2")
                            break_start = ebl.get("start")
                            break_end = ebl.get("end")
                            time_diff = self.time_diff_mins(break_start, ts)
                            display_ts = self.mins_pp(time_diff)
                            reason = (f"{username} has break status at "
                                      f"{ts_pp} when break finish expected "
                                      f"at {self.pp_date(break_end)}")
                            self.set_alarm(username, ts, display_ts,
                                           {"start": break_start}, event,
                                           reason, ttl)
                            break


class SIU(Alarm):
    '''
    Sign In Unexpectedly
    Alarm is set when an agent logs in after
        shift end + esl.window + grace
    or agent logs in before
        shift start - bse.window - grace
    of agent logs in and there is no schedule for them
    '''

    def __init__(self, schedules):
        super().__init__("SIU", ["LOGIN"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if not state:
                event = self.typed_event("LOGIN", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    agent_state = self.agent_state(event)
                    windows = self.get_alarm_times(username, True)

                    ts = event.get("EventTimestamp")
                    display_ts = self.pp_date(ts)
                    if not self.schedules.get(username):
                        reason = (f"{username} logged in at {display_ts} "
                                  f" but no schedule exists for them")
                        self.set_alarm(username, ts, display_ts, {},
                                       event, reason)
                        return

                    for window in windows:

                        if self.before(window.get("T1"), event):
                            reason = (f"{username} logged in at {display_ts} "
                                      f"before their expected shift start "
                                      f"time of {window.get('start')}")
                            self.set_alarm(username, ts, display_ts, {},
                                           event, reason)
                            break
                        if self.after(window.get("T2"), event):
                            reason = (f"{username} logged in at {display_ts} "
                                      f"after their expected shift ended "
                                      f"time of {self.pp_date(window.get('end'))}")
                            self.set_alarm(username, ts, display_ts, {},
                                           event, reason)
                            break


class SOU(Alarm):
    '''
    Sign Out Unexpectedly
    Alarm is set when an agent logs out before
        shift end - ese.window - grace
    '''

    def __init__(self, schedules):
        super().__init__("SOU", ["HEART_BEAT", "LOGOUT", "LOGIN"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if state:
                '''Clear alarm conditions'''
                event = self.typed_event("HEART_BEAT", filtered_events)

                shift_end = state.get("end")
                if event and shift_end and self.after(shift_end, event):
                    self.clear_alarm(username)
                event = self.typed_event("LOGIN", filtered_events)
                if event:
                    self.clear_alarm(username)

            if not state:
                event = self.typed_event("LOGOUT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    windows = self.get_alarm_times(username, True)
                    for window in windows:
                        if self.before(window.get("T1"), event):
                            ts = event.get("EventTimestamp")
                            display_ts = self.pp_date(ts)
                            reason = (f"{username} logged out at {display_ts} "
                                      f"before expected end of shift at "
                                      f"{self.pp_date(window.get('end'))}")
                            self.set_alarm(username, ts, display_ts,
                                           {"end": window.get("end")},
                                           event, reason)
                            break


class WOB(Alarm):
    '''
    Working On Break
    Alarm is set when an agent is available between
        break start time + grace (T1) and break end time - grace (T2)

    Alarm clears at T2
    '''

    def __init__(self, schedules):
        super().__init__("WOB", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:

            if state:
                '''Incremental display ts'''
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    event_ts = event.get("EventTimestamp")
                    shift_start = self.shift_start(username)
                    break_start = state.get("extra", {}).get("start")
                    time_diff = self.time_diff_mins(event_ts, break_start)
                    display_ts = self.mins_pp(time_diff)
                    self.update_display_ts(username, display_ts)

            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    wobs = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)
                    for wob in wobs:
                        if self.is_between(wob, event) \
                           and agent_state not in self.BREAK_CODES:
                            ts = event.get("EventTimestamp")
                            ts_pp = self.pp_date(ts)
                            time_diff = self.time_diff_mins(ts, wob.get("start"))
                            display_ts = self.mins_pp(time_diff)
                            ttl = wob.get("T2")
                            reason = (f"{username} has not set a break status "
                                      f" at {ts_pp}, break start expected at "
                                      f"{self.pp_date(wob.get('start'))}")
                            self.set_alarm(username, ts, display_ts,
                                           {"start": wob.get("start")},
                                           event, reason, ttl)
                            break


class BXE(Alarm):
    '''
    Begin Exception Early
    Alarm is set when an agent enters state of
    'System Down', 'Admin', 'Training' or '121'
    between
        exception start time - window (T1) and exception start time - grace (T2)

    '''

    def __init__(self, schedules):
        super().__init__("BXE", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    bees = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)
                    for bee in bees:
                        if self.is_between(bee, event) \
                           and agent_state in self.EXCEPTION_CODES:
                            ts = event.get("EventTimestamp")
                            ts_pp = self.pp_date(ts)
                            exc_start = bee.get("start")

                            time_diff = self.time_diff_mins(exc_start, ts)
                            display_ts = self.mins_pp(time_diff)
                            ttl = bee.get("T2")
                            reason = (f"{username} has set an exception "
                                      f"status at {ts_pp} when exception "
                                      f"should start at "
                                      f"{self.pp_date(exc_start)}")
                            self.set_alarm(username, ts, display_ts, {},
                                           event, reason, ttl)
                            break


class EXL(Alarm):
    '''
    End Exception Late
    Alarm is set when an agent is in Exception code between
        exception end time + grace (T1) and exception end time + window (T2)

    Alarm cleared at break end + window (T2)
    '''

    def __init__(self, schedules):
        super().__init__("EXL", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:

            if state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    '''Incremental display ts'''
                    event_ts = event.get("EventTimestamp")
                    shift_start = self.shift_start(username)
                    time_diff = self.time_diff_mins(event_ts, state.get("end"))
                    display_ts = self.mins_pp(time_diff)
                    self.update_display_ts(username, display_ts)

            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    exls = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)

                    for exl in exls:
                        if self.is_between(exl, event) \
                           and agent_state in self.EXCEPTION_CODES:
                            ts = event.get("EventTimestamp")
                            ts_pp = self.pp_date(ts)
                            ttl = exl.get("T2")
                            display_ts = datetime.strftime(self.get_ts(ttl),
                                                           '%H:%M:%S %d/%m/%Y')
                            reason = (f"{username} has an exception status "
                                      f"at {ts_pp} where exception should "
                                      f"have ended at "
                                      f"{self.pp_date(exl.get('end'))}")
                            self.set_alarm(username, ts, display_ts,
                                           {"end": exl.get("T2")},
                                           event, reason, ttl)
                            break


class WOE(Alarm):
    '''
    Working On Exception
    Alarm is set when an agent is available between
        exception start time + grace (T1) and exceptoin end time - grace (T2)

    Alarm clears at T2
    '''

    def __init__(self, schedules):
        super().__init__("WOE", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if state:
                '''Incremental display ts'''
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    event_ts = event.get("EventTimestamp")
                    shift_start = self.shift_start(username)
                    exception_start = state.get("extra", {}).get("start")
                    time_diff = self.time_diff_mins(event_ts,
                                                    exception_start)
                    display_ts = self.mins_pp(time_diff)
                    self.update_display_ts(username, display_ts)

            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    woes = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)
                    for woe in woes:
                        if self.is_between(woe, event) \
                           and agent_state not in self.EXCEPTION_CODES:
                            ts = event.get("EventTimestamp")
                            ts_pp = self.pp_date(ts)
                            time_diff = self.time_diff_mins(ts,
                                                            woe.get("start"))

                            display_ts = self.mins_pp(time_diff)
                            ttl = woe.get("T2")
                            reason = (f"{username} has a status of "
                                      f"{agent_state} at {ts_pp}, "
                                      f"expecting an exception "
                                      f"status by "
                                      f"{self.pp_date(woe.get('start'))}")
                            self.set_alarm(username, ts, display_ts,
                                           {"start": woe.get("start")},
                                           event, reason, ttl)
                            break
