from datetime import datetime
from datetime import timedelta
import boto3
import logging
import json
from botocore.exceptions import ClientError
import os


logger = logging.getLogger()
# INFO = 20
# DEBUG = 10
LOGGING_LEVEL = int(os.environ.get("LOGGING_LEVEL", "20"))
logger.setLevel(LOGGING_LEVEL)


class Alarm:

    BREAK_CODES = ["Break", "Lunch"]
    EXCEPTION_CODES = ['System Down', 'Admin', 'Training', '121']
    EVENT_TYPES = ['SP_HEART_BEAT', 'STATE_CHANGE', 'LOGIN', 'LOGOUT']

    def __init__(self, alarmcode, event_types, schedules):
        self.alarmcode = alarmcode
        self.event_types = event_types
        self.schedules = schedules

    def filter(self, events):
        return [event for event in events
                if event.get("EventType") in self.event_types]

    def create_set_alarm(self, username, ts, display_ts, extra,
                         trigger, reason, ttl=None):
        logger.info(f"Creating new alarm {self.alarmcode} for {username}"
                    f" at {ts} with TTL {ttl}: {display_ts} "
                    f" extra: {str(extra)}"
                    f" reason: {reason}")

        logger.info(f"@ALARM|SET_ALARM|{username}|{self.alarmcode}|"
                    f"{ts}|{reason}")
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
        return {
            "type": "put",
            "item": item
        }

    def create_clear_alarm(self, username):
        logger.info(f"Creating clear alarm {self.alarmcode} for {username}")
        logger.info(f"@ALARM|CLEAR_ALARM|{username}|{self.alarmcode}")
        return {
            "type": "delete",
            "key": {"username": username, "alarmcode": self.alarmcode}
        }

    def create_update_display_ts(self, username, display_ts):
        logger.info(f"Creating update alarm {self.alarmcode} display ts "
                    f"for user {username} to {display_ts}")
        logger.info(f"@ALARM|UPDATE_ALARM|{username}|{self.alarmcode}|"
                    f"{display_ts}")

        return {
            "type": "update",
            "key": {"username": username, "alarmcode": self.alarmcode},
            "field": "display_ts",
            "val": display_ts
        }

    def agent_state(self, event):
        return event.get("CurrentAgentSnapshot", {}) \
                    .get("AgentStatus", {}) \
                    .get("Name")

    def get_alarm_times(self, username, asList=False):
        if not self.schedules.get(username):
            logger.info(f"No schedule found for {username}")
            return []

        alarms = self.schedules.get(username).get('ALARMS')
        if not alarms.get(self.alarmcode):
            logger.debug(f"No alarm params exist for user {username}")
            return {}
        if asList:
            return alarms.get(self.alarmcode)
        else:
            return alarms.get(self.alarmcode)[0]

    def get_schedule(self, username, code="SHIFT"):
        return self.schedules.get(username).get('SCHEDULE').get(code)

    def process(self, events, username, state, history=None):
        filtered_events = self.filter(events)
        if filtered_events:
            if state:
                return self.process_alarm_active(filtered_events, username,
                                          state, history)
            else:
                return self.process_alarm_inactive(filtered_events, username,
                                            state, history)

    def process_alarm_active(self, _events, _username, _state, _history):
        pass

    def process_alarm_inactive(self, _events, _username, _state, _history):
        pass

    # Time related static methods

    @staticmethod
    def get_ts(ts):
        if not ts:
            return "-"
        try:
            ts1 = datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')
        except Exception:
            ts1 = datetime.strptime(ts, '%Y-%m-%dT%H:%M')
        return ts1

    @staticmethod
    def is_between(w, event):
        if not event:
            return False

        t1 = Alarm.get_ts(w.get("T1"))
        t2 = Alarm.get_ts(w.get("T2"))
        event_ts = Alarm.get_ts(event.get("EventTimestamp"))
        result = t1 < event_ts < t2
        return result

    @staticmethod
    def after(ts, event):
        if not event:
            return False
        t = Alarm.get_ts(ts)
        event_ts = Alarm.get_ts(event.get("EventTimestamp"))
        return event_ts > t

    @staticmethod
    def before(ts, event):
        if not event:
            return False
        event_ts = Alarm.get_ts(event.get("EventTimestamp"))
        t = Alarm.get_ts(ts)
        return event_ts < t

    @staticmethod
    def typed_event(typ, events):
        for event in events:
            if event.get("EventType") == typ:
                return event
        return None

    @staticmethod
    def time_diff_mins(t1, t2):

        ts1 = Alarm.get_ts(t1)
        ts2 = Alarm.get_ts(t2)

        if ts1 and ts2:
            diff = ts1 - ts2
            return abs(int(divmod(diff.total_seconds(), 60)[0]))
        else:
            raise Exception(f"Time parse exception in time_diff_mins with "
                            f"t1={t1} and t2={t2}")

    @staticmethod
    def mins_pp(mins):
        if not mins:
            return "00:00"
        (hours, minutes) = divmod(mins, 60)
        return f"{hours:02d}:{minutes:02d}"

    @staticmethod
    def pp_date(date):
        d = Alarm.get_ts(date)
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
        super().__init__("BSE", ["LOGIN", "SP_HEART_BEAT"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:
            if state:
                '''Clear alarm conditions'''
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if state.get("extra", {}).get("end"):
                    if Alarm.after(state.get("extra", {}).get("end"), event):
                        db_updates.append(self.create_clear_alarm(username))

            if not state:
                '''Set alarm conditions'''
                event = Alarm.typed_event("LOGIN", filtered_events)
                if event:
                    windows = self.get_alarm_times(username, True)
                    for window in windows:
                        if Alarm.is_between(window, event):
                            ts = event.get("EventTimestamp")
                            ts_pp = datetime.strftime(self.get_ts(ts),
                                                      '%H:%M:%S %d/%m/%Y')
                            shift_start = window.get("start")
                            shift_end = window.get("end")
                            time_diff = Alarm.time_diff_mins(shift_start, ts)
                            display_ts = Alarm.mins_pp(time_diff)
                            ttl = shift_end
                            reason = (f"{username} login at {ts_pp} "
                                      f"before shift start at "
                                      f"{Alarm.pp_date(shift_start)}")
                            
                            db_update = self.create_set_alarm(username, ts, display_ts,
                                                              {"end": window.get("T2")},
                                                              event, reason, ttl)
                            print(f"update: {str(db_update)}")
                            db_updates.append(db_update)
                            break
        return db_updates


class BSL(Alarm):
    '''
    Begin Shift Late

    Alarm is set when agent has state 'Offline' between
        shift start time + grace and shift end time

    Alarm cleared on agent login or end of shift
    '''

    def __init__(self, schedules):
        super().__init__("BSL",
                         ["LOGIN", "SP_HEART_BEAT"],
                         schedules)

    def process_alarm_active(self, events, username, state, history):
        '''Incremental display ts'''
        event = Alarm.typed_event("LOGIN", events)
        db_updates = []
        if event:
            logger.info(f"@BSL {username} LOGIN detected")
            extra = state.get("extra", {})
            extra['BSL_LOGIN'] = "1"
            shift_start = extra.get("start")
            logger.info(f"@BSL Updating extra for alarm: {extra}")
            ts = event.get("EventTimestamp")
            reason = (f"{username} was late logging in: "
                      f"shift expected to start at "
                      f"{Alarm.pp_date(shift_start)} "
                      f"but agent signed in at {Alarm.pp_date(ts)}")
            db_updates.append({
                "type": "update",
                "key": {"username": username, "alarmcode": self.alarmcode},
                "field": "extra",
                "val": extra
            })
            db_updates.append({
                "type": "update",
                "key": {"username": username, "alarmcode": self.alarmcode},
                "field": "reason",
                "val": reason
            })

        else:
            event = Alarm.typed_event("SP_HEART_BEAT", events)
            if event:
                user_already_logged_in = [
                    h for h in history
                    if h.get("username") == username and
                    h.get("prop") == "LOGIN"
                ]
                if user_already_logged_in:
                    logger.info(f"@BSL {username} LOGIN detected in history")
                else:
                    logger.info(f"@BSL {username} expect ts increment")
                    logger.info(f"@BSL {username} state={state}")
                    logger.info(f"@BSL {username} state.extra={state.get('extra')}")
                    event_ts = event.get("EventTimestamp")
                    shift_start = state.get("extra", {}).get("start")
                    time_diff = Alarm.time_diff_mins(shift_start, event_ts)
                    display_ts = Alarm.mins_pp(time_diff)
                    db_updates.append(self.create_update_display_ts(username, display_ts))
        return db_updates

    def process_alarm_inactive(self, events, username, state, history):
        '''Set alarm conditions'''

        event = Alarm.typed_event("SP_HEART_BEAT", events)

        db_updates = []
        if event:
            # ignore LOGIN event if user has already logged in
            # previously (captured in history)
            user_already_logged_in = [
                h for h in history
                if h.get("username") == username and
                h.get("prop") == "LOGIN"
            ]
            logger.debug(f"BSL: User logged in already: "
                         f"{user_already_logged_in}")

            if user_already_logged_in:
                return db_updates

            # calculate whether heartbeat falls inside
            # BSL window(s)
            windows = self.get_alarm_times(username, True)
            for window in windows:
                if Alarm.is_between(window, event):
                    ts = event.get("EventTimestamp")
                    ts_pp = Alarm.pp_date(ts)
                    shift_start = window.get("start")
                    time_diff = Alarm.time_diff_mins(shift_start, ts)
                    display_ts = Alarm.mins_pp(time_diff)
                    reason = (f"{username} has not logged in yet at "
                              f"{ts_pp}, shift start at "
                              f"{Alarm.pp_date(shift_start)}")

                    extra = {
                        "start": window.get('start'),
                        "end": window.get('end')
                    }
                    db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                                            extra, event, reason))
                    break
        return db_updates


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

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:
            if not state:
                '''Set alarm conditions'''
                event = Alarm.typed_event("LOGOUT", filtered_events)
                if event:
                    ts = event.get("EventTimestamp")
                    windows = self.get_alarm_times(username, True)
                    for window in windows:
                        if Alarm.before(window.get("T1"), event):
                            # the reported time shift end time
                            ts_pp = Alarm.pp_date(ts)
                            shift_end = window.get("end")
                            time_diff = Alarm.time_diff_mins(ts, shift_end)
                            display_ts = Alarm.mins_pp(time_diff)
                            ttl = shift_end
                            reason = (f"{username} logged out at {ts_pp} "
                                      f"before shift end at "
                                      f"{Alarm.pp_date(shift_end)}")

                            db_updates.append(self.create_set_alarm(username, ts, display_ts, {},
                                                             event, reason, ttl))
        return db_updates


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
        super().__init__("ESL", ["SP_HEART_BEAT"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:

            if state:
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                '''Incremental display ts'''
                if event and self.agent_state(event) != "Offline":
                    ts = event.get("EventTimestamp")
                    shift_end = state.get("extra", {}).get("end")
                    time_diff = Alarm.time_diff_mins(shift_end, ts)
                    display_ts = Alarm.mins_pp(time_diff)
                    db_updates.append(self.create_update_display_ts(username, display_ts))

                '''Clear alarm conditions'''
                if event and self.agent_state(event) == "Offline":
                    db_updates.append(self.create_clear_alarm(username))

            if not state:
                '''Set alarm conditions'''
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if event:
                    if self.agent_state(event) != "Offline":
                        windows = self.get_alarm_times(username, True)
                        for window in windows:
                            if Alarm.is_between(window, event):
                                # the reported time shift end time
                                ts = event.get("EventTimestamp")
                                ts_pp = Alarm.pp_date(ts)
                                shift_end = window.get("end")
                                time_diff = Alarm.time_diff_mins(shift_end, ts)
                                display_ts = Alarm.mins_pp(time_diff)
                                ttl = window.get("T2")
                                reason = (f"{username} not offline at {ts_pp} "
                                          f"after end of shift at "
                                          f"{Alarm.pp_date(shift_end)}")
                                db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                                 {"end": window.get("end")},
                                                 event, reason, ttl))
                                break
        
        return db_updates

class BBE(Alarm):
    '''
    Begin Break Early
    Alarm is set when an agent enters state of
    'Break' or 'Lunch'
    between
        break start time - window (T1) and break start time - grace (T2)

    '''

    def __init__(self, schedules):
        super().__init__("BBE", ["STATE_CHANGE"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:
            if not state:
                event = Alarm.typed_event("STATE_CHANGE", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    agent_state = self.agent_state(event)
                    if agent_state in self.BREAK_CODES:
                        bbes = self.get_alarm_times(username, True)
                        for bbe in bbes:
                            if Alarm.is_between(bbe, event) \
                               and agent_state in self.BREAK_CODES:
                                ts = event.get("EventTimestamp")
                                ts_pp = Alarm.pp_date(ts)
                                break_start = bbe.get("start")
                                time_diff = Alarm.time_diff_mins(break_start, ts)
                                display_ts = Alarm.mins_pp(time_diff)
                                ttl = bbe.get("end")
                                reason = (f"{username} entered break at {ts_pp} "
                                          f"earlier than expected start "
                                          f"time of "
                                          f"{Alarm.pp_date(break_start)}")
                                db_updates.append(self.create_set_alarm(username, ts, display_ts, {},
                                               event, reason, ttl))
                                break

        return db_updates

class EBL(Alarm):
    '''
    End Break Late
    Alarm is set when an agent is a status of break between
        break end time + grace (T1) and break end time + window (T2)

    Alarm cleared at break end + window (T2)
    '''

    def __init__(self, schedules):
        super().__init__("EBL", ["SP_HEART_BEAT"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:
            if state:
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                break_end = state.get("extra", {}).get("end")
                agent_state = self.agent_state(event)
                if event and break_end and agent_state in self.BREAK_CODES:
                    event_ts = event.get("EventTimestamp")
                    time_diff = Alarm.time_diff_mins(break_end, event_ts)
                    display_ts = Alarm.mins_pp(time_diff)
                    db_updates.append(self.create_update_display_ts(username, display_ts))

            if not state:
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    ebls = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)
                    for ebl in ebls:
                        if Alarm.is_between(ebl, event) and \
                           agent_state in self.BREAK_CODES:
                            ts = event.get("EventTimestamp")
                            ts_pp = Alarm.pp_date(ts)
                            ttl = ebl.get("T2")
                            break_start = ebl.get("start")
                            break_end = ebl.get("end")
                            time_diff = Alarm.time_diff_mins(break_end, ts)
                            display_ts = Alarm.mins_pp(time_diff)
                            reason = (f"{username} has break status at "
                                      f"{ts_pp} when break finish expected "
                                      f"at {Alarm.pp_date(break_end)}")
                            db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                                            {
                                                                "start": break_start,
                                                                "end": break_end
                                                            }, event,
                                                            reason, ttl))
                            break

        return db_updates

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
        super().__init__("SIU", ["LOGIN", "SP_HEART_BEAT"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:
            if state:
                event = Alarm.typed_event("SP_HEART_BEAT")
                if event:
                    '''Incremental ts update'''
                    ts = event.get("EventTimestamp")
                    login_ts = state.get("extra",{}).get("login")
                    if login_ts:
                        logger.info("SIU ts updating")
                        time_diff = Alarm.time_diff_mins(login_ts, ts)
                        display_ts = Alarm.mins_pp(time_diff)
                        db_updates.append(self.create_update_display_ts(username, display_ts))

            if not state:
                event = Alarm.typed_event("LOGIN", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    agent_state = self.agent_state(event)
                    windows = self.get_alarm_times(username, True)

                    ts = event.get("EventTimestamp")
                    display_ts = Alarm.pp_date(ts)
                    if not self.schedules.get(username):
                        reason = (f"{username} logged in at {display_ts} "
                                  f" but no schedule exists for them")
                        db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                          {"login": ts},
                                          event, reason))
                        return db_updates

                    for window in windows:

                        if Alarm.before(window.get("T1"), event):
                            reason = (f"{username} logged in at {display_ts} "
                                      f"before their expected shift start "
                                      f"time of {window.get('start')}")
                            db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                              {"login": ts},
                                              event, reason))
                            break
                        if Alarm.after(window.get("T2"), event):
                            reason = (f"{username} logged in at {display_ts} "
                                      f"after their expected shift ended "
                                      f"time of "
                                      f"{Alarm.pp_date(window.get('end'))}")
                            db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                              {"login": ts},
                                              event, reason))
                            break

        return db_updates

class SOU(Alarm):
    '''
    Sign Out Unexpectedly
    Alarm is set when an agent logs out before
        shift end - ese.window - grace
    '''

    def __init__(self, schedules):
        super().__init__("SOU", ["SP_HEART_BEAT", "LOGOUT", "LOGIN"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:
            if state:
                '''Clear alarm conditions'''
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                shift_end = state.get("extra", {}).get("end")
                if event and shift_end and Alarm.after(shift_end, event):
                    db_updates.append(self.create_clear_alarm(username))
                
                event = Alarm.typed_event("LOGIN", filtered_events)
                if event:
                    db_updates.append(self.create_clear_alarm(username))
                    return db_updates
                
                '''Update incremental ts'''
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                ts = event.get("EventTimestamp")
                logout_ts = state.get("extra", {}).get("logout")
                if event and logout_ts:
                    time_diff = Alarm.time_diff_mins(logout_ts, ts)
                    display_ts = Alarm.mins_pp(time_diff)
                    db_updates.append(self.create_update_display_ts(username, display_ts))

            if not state:
                event = Alarm.typed_event("LOGOUT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    windows = self.get_alarm_times(username, True)
                    for window in windows:
                        if Alarm.is_between(window, event):
                        # if Alarm.before(window.get("T1"), event):
                            ts = event.get("EventTimestamp")
                            display_ts = Alarm.pp_date(ts)
                            reason = (f"{username} logged out at {display_ts} "
                                      f"before expected end of shift at "
                                      f"{Alarm.pp_date(window.get('end'))}")
                            db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                              {"end": window.get("end"), "logout": ts},
                                              event, reason))
                            break

        return db_updates

class WOB(Alarm):
    '''
    Working On Break
    Alarm is set when an agent is available between
        break start time + grace (T1) and break end time - grace (T2)

    Alarm clears at T2
    '''

    def __init__(self, schedules):
        super().__init__("WOB", ["SP_HEART_BEAT"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:

            if state:
                '''Incremental display ts'''
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if event:
                    logger.info(f"@WOB|Incremental ts|Current state={state}")
                    event_ts = event.get("EventTimestamp")
                    break_start = state.get("extra", {}).get("start")
                    time_diff = Alarm.time_diff_mins(event_ts, break_start)
                    display_ts = Alarm.mins_pp(time_diff)
                    db_updates.append(self.create_update_display_ts(username, display_ts))

            if not state:
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    wobs = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)
                    for wob in wobs:
                        if Alarm.is_between(wob, event) \
                           and agent_state not in self.BREAK_CODES \
                           and agent_state != "Offline":
                            ts = event.get("EventTimestamp")
                            ts_pp = Alarm.pp_date(ts)
                            time_diff = Alarm.time_diff_mins(ts,
                                                             wob.get("start"))
                            display_ts = Alarm.mins_pp(time_diff)
                            ttl = wob.get("T2")
                            reason = (f"{username} has not set a break status "
                                      f" at {ts_pp}, break start expected at "
                                      f"{Alarm.pp_date(wob.get('start'))}")
                            logger.info(f"@WOB|Set alarm|reason={reason}")
                            db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                              {"start": wob.get("start")},
                                              event, reason, ttl))
                            break
        
        return db_updates

class BXE(Alarm):
    '''
    Begin Exception Early
    Alarm is set when an agent enters state of
    'System Down', 'Admin', 'Training' or '121'
    between
        exception start time - window (T1) and
        exception start time - grace (T2)

    '''

    def __init__(self, schedules):
        super().__init__("BXE", ["SP_HEART_BEAT"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:
            if not state:
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    bees = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)
                    for bee in bees:
                        if Alarm.is_between(bee, event) \
                           and agent_state in self.EXCEPTION_CODES:
                            ts = event.get("EventTimestamp")
                            ts_pp = Alarm.pp_date(ts)
                            exc_start = bee.get("start")

                            time_diff = Alarm.time_diff_mins(exc_start, ts)
                            display_ts = Alarm.mins_pp(time_diff)
                            ttl = bee.get("T2")
                            reason = (f"{username} has an exception status "
                                      f"{agent_state} at {ts_pp} when "
                                      f" exception expected to start at "
                                      f"{Alarm.pp_date(exc_start)}")
                            db_updates.append(self.create_set_alarm(username, ts, display_ts, {},
                                              event, reason, ttl))
                            break

        return db_updates

class EXL(Alarm):
    '''
    End Exception Late
    Alarm is set when an agent is in Exception code between
        exception end time + grace (T1) and exception end time + window (T2)

    Alarm cleared at break end + window (T2)
    '''

    def __init__(self, schedules):
        super().__init__("EXL", ["SP_HEART_BEAT"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:

            if state:
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if event:
                    '''Incremental display ts'''
                    event_ts = event.get("EventTimestamp")
                    exception_end = state.get("extra", {}).get("end")
                    time_diff = Alarm.time_diff_mins(event_ts, exception_end)
                    display_ts = Alarm.mins_pp(time_diff)
                    db_updates.append(self.create_update_display_ts(username, display_ts))

            if not state:
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    exls = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)

                    for exl in exls:
                        if Alarm.is_between(exl, event) \
                           and agent_state in self.EXCEPTION_CODES:
                            ts = event.get("EventTimestamp")
                            ts_pp = Alarm.pp_date(ts)
                            ttl = exl.get("T2")
                            display_ts = datetime.strftime(self.get_ts(ttl),
                                                           '%H:%M:%S %d/%m/%Y')
                            reason = (f"{username} has an exception status "
                                      f"of {agent_state} "
                                      f"at {ts_pp} where exception should "
                                      f"have ended at "
                                      f"{Alarm.pp_date(exl.get('end'))}")
                            db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                              {"end": exl.get("T2")},
                                              event, reason, ttl))
                            break

        return db_updates

class WOE(Alarm):
    '''
    Working On Exception
    Alarm is set when an agent is available between
        exception start time + grace (T1) and exception end time - grace (T2)

    Alarm clears at T2
    '''

    def __init__(self, schedules):
        super().__init__("WOE", ["SP_HEART_BEAT"], schedules)

    def process(self, events, username, state, _history=[]):
        filtered_events = self.filter(events)
        db_updates = []
        if filtered_events:
            if state:
                '''Incremental display ts'''
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if event:
                    event_ts = event.get("EventTimestamp")
                    exception_start = state.get("extra", {}).get("start")
                    time_diff = Alarm.time_diff_mins(event_ts,
                                                     exception_start)
                    display_ts = Alarm.mins_pp(time_diff)
                    db_updates.append(self.create_update_display_ts(username, display_ts))

            if not state:
                event = Alarm.typed_event("SP_HEART_BEAT", filtered_events)
                if event:
                    '''Set alarm conditions'''
                    woes = self.get_alarm_times(username, True)
                    agent_state = self.agent_state(event)
                    for woe in woes:
                        if Alarm.is_between(woe, event) \
                           and agent_state not in self.EXCEPTION_CODES \
                           and agent_state not in self.BREAK_CODES \
                           and agent_state != "Offline":
                            ts = event.get("EventTimestamp")
                            ts_pp = Alarm.pp_date(ts)
                            time_diff = Alarm.time_diff_mins(ts,
                                                             woe.get("start"))

                            display_ts = Alarm.mins_pp(time_diff)
                            ttl = woe.get("T2")
                            reason = (f"{username} has a status of "
                                      f"{agent_state} at {ts_pp}; "
                                      f"exception scheduled for "
                                      f"{Alarm.pp_date(woe.get('start'))}"
                                      f"- {Alarm.pp_date(woe.get('end'))}")
                            db_updates.append(self.create_set_alarm(username, ts, display_ts,
                                              {"start": woe.get("start")},
                                              event, reason, ttl))
                            break

        return db_updates
