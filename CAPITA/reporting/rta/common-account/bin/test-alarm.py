from datetime import datetime
from datetime import timedelta
from time import sleep


class Alarm:

    def __init__(self, alarmcode, event_types, schedules):
        self.alarmcode = alarmcode
        self.event_types = event_types
        self.schedules = schedules

    def filter(self, events):
        return [event for event in events
                if event.get("EventType") in self.event_types]

    def is_between(self, window, event):
        if not event:
            return False
        result = window.get("T1") < event.get("EventTimestamp") < window.get("T2")
        return result

    def after(self, ts, event):
        if not event:
            return False
        result = event.get("EventTimestamp") > ts
        print(f"{self.alarmcode}: {str(event.get('EventTimestamp'))} > {str(ts)} = {result}")
        return result

    def before(self, ts, event):
        if not event:
            return False
        result = event.get("EventTimestamp") < ts
        print(f"{self.alarmcode}: {str(event.get('EventTimestamp'))} < {str(ts)} = {result}")
        return result

    def set_alarm(self, username, ts, ttl=None):
        print(f"Setting alarm {self.alarmcode} for {username} at {ts} with TTL {ttl}")

    def clear_alarm(self, username):
        print(f"Clearing alarm {self.alarmcode} for {username}")

    def typed_event(self, typ, events):
        for event in events:
            if event.get("EventType") == typ:
                return event
        return None

    def agent_state(self, event):
        return event.get("CurrentAgentSnapshot", {}) \
                    .get("AgentStatus", {}) \
                    .get("Name")

    def get_alarm_times(self, username):
        alarms = self.schedules.get(username).get('ALARMS')
        if not alarms.get(self.alarmcode):
            print(f"No alarm params exist for user {username}")
            return {}
        return alarms.get(self.alarmcode)

    def get_schedule(self, username, code="SHIFT"):
        return self.schedules.get(username).get('SCHEDULE').get(code)


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
                alarm_times = self.get_alarm_times(username)
                if self.after(alarm_times.get("T2"), event):
                    self.clear_alarm(username)

            if not state:
                '''Set alarm conditions'''
                event = self.typed_event("LOGIN", filtered_events)
                alarm_times = self.get_alarm_times(username)
                if self.is_between(alarm_times, event):
                    rts = event.get("EventTimestamp")
                    ttl = alarm_times.get("T2")
                    self.set_alarm(username, rts, ttl)


class BSL(Alarm):
    '''
    Begin Shift Late
    Alarm is set when agent signs in after
        shift start time + grace

    Alarm cleared on agent login or end of shift
    '''

    def __init__(self, schedules):
        super().__init__("BSL", ["LOGIN", "HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if state:
                '''Clear alarm conditions'''
                event = self.typed_event("HEART_BEAT", filtered_events)
                t2 = self.get_schedule(username).get("T2")
                if self.after(t2, event):
                    self.clear_alarm(username)

            if not state:
                '''Set alarm conditions'''
                event = self.typed_event("LOGIN", filtered_events)
                alarm_times = self.get_alarm_times(username)
                if self.after(alarm_times.get("T1"), event):
                    # the reported time is one minute past the expected shift start time
                    rts = self.get_schedule(username).get("T1") + timedelta(minutes=1)
                    self.set_alarm(username, rts)


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
                alarm_times = self.get_alarm_times(username)
                ts = alarm_times.get("T1")
                if self.before(ts, event):
                    # the reported time shift end time
                    rts = self.get_schedule(username).get("T2")
                    ttl = alarm_times.get("T1")
                    self.set_alarm(username, rts, ttl)


class ESL(Alarm):
    '''
    End Shift Late
    Alarm is set when agent is still logged in between
        shift end time + grace (T1) and shift end time + window (T2)

    Reported time is event timestamp

    Alarm is cleared by TTL after
        shift end time
    '''

    def __init__(self, schedules):
        super().__init__("ESL", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if not state:
                '''Set alarm conditions'''
                event = self.typed_event("HEART_BEAT", filtered_events)

                if self.agent_state(event) == "Available":
                    alarm_times = self.get_alarm_times(username)
                    if self.is_between(alarm_times, event):
                        # the reported time shift end time
                        rts = event.get("EventTimestamp")
                        ttl = self.get_schedule(username).get("T2")
                        self.set_alarm(username, rts, ttl)


class BBE(Alarm):
    '''
    Begin Break Early
    Alarm is set when an agent is not available between
        break start time - window (T1) and break start time - grace (T2)

    '''

    def __init__(self, schedules):
        super().__init__("BBE", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                '''Set alarm conditions'''
                bbes = self.get_alarm_times(username)
                agent_state = self.agent_state(event)
                for bbe in bbes:
                    if self.is_between(bbe, event) and agent_state != "Available":
                        rts = event.get("EventTimestamp")
                        ttl = bbe.get("T2")
                        self.set_alarm(username, rts, ttl)
                        break


class EBL(Alarm):
    '''
    End Break Late
    Alarm is set when an agent is not available between
        break end time + grace (T1) and break end time + window (T2)

    '''

    def __init__(self, schedules):
        super().__init__("EBL", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                '''Set alarm conditions'''
                ebls = self.get_alarm_times(username)
                agent_state = self.agent_state(event)
                for ebl in ebls:
                    if self.is_between(ebl, event) and agent_state != "Available":
                        rts = event.get("EventTimestamp")
                        ttl = ebl.get("T2")
                        self.set_alarm(username, rts, ttl)
                        break


class SIU(Alarm):
    '''
    Sign In Unexpectedly
    Alarm is set when an agent is available after
        shift end + window
    '''

    def __init__(self, schedules):
        super().__init__("SIU", ["HEART_BEAT"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                '''Set alarm conditions'''
                agent_state = self.agent_state(event)
                alarm_times = self.get_alarm_times(username)
                if self.after(alarm_times.get("T1"), event) \
                   and agent_state == "Available":
                    rts = event.get("EventTimestamp")
                    self.set_alarm(username, rts)


class SOU(Alarm):
    '''
    Sign Out Unexpectedly
    Alarm is set when an agent logs out before
        shift end - grace
    '''

    def __init__(self, schedules):
        super().__init__("SOU", ["HEART_BEAT", "LOGOUT", "LOGIN"], schedules)

    def process(self, events, username, state):
        filtered_events = self.filter(events)
        if filtered_events:
            if state:
                '''Clear alarm conditions'''
                event = self.typed_event("HEART_BEAT", filtered_events)
                shift_end = self.get_schedule(username).get("T2")
                if event and self.after(shift_end, event):
                    self.clear_alarm(username)
                event = self.typed_event("LOGIN", filtered_events)
                if event:
                    self.clear_alarm(username)

            if not state:
                event = self.typed_event("LOGOUT", filtered_events)
                '''Set alarm conditions'''
                alarm_times = self.get_alarm_times(username)
                if self.before(alarm_times.get("T1"), event):
                    rts = event.get("EventTimestamp")
                    self.set_alarm(username, rts)


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
            if not state:
                event = self.typed_event("HEART_BEAT", filtered_events)
                '''Set alarm conditions'''
                wobs = self.get_alarm_times(username)
                agent_state = self.agent_state(event)
                for wob in wobs:
                    if self.is_between(wob, event) \
                       and agent_state == "Available":
                        rts = event.get("EventTimestamp")
                        ttl = wob.get("T2")
                        self.set_alarm(username, rts, ttl)
                        break


def create_event(typ, username, ts, status='Available'):
    return [
        {
            "EventType": typ,
            "CurrentAgentSnapshot": {
                "Configuration": {
                    "Username": username
                },
                "AgentStatus": {
                    "Name": status
                }
            },
            "EventTimestamp": datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')
        }
    ]


# calculated schedule for ONE agent
schedule = {
    "P0001": {
        "SCHEDULE": {
            "SHIFT": {
                # shift 08:00 - 16:30
                "T1": datetime.strptime("2019-01-21T08:00", '%Y-%m-%dT%H:%M'),
                "T2": datetime.strptime("2019-01-21T16:30", '%Y-%m-%dT%H:%M')
            }
        },
        "ALARMS": {
            "BSE": {
                # 07:30 - 07:55
                "T1": datetime.strptime("2019-01-21T07:30", '%Y-%m-%dT%H:%M'),
                "T2": datetime.strptime("2019-01-21T07:55", '%Y-%m-%dT%H:%M')
            },
            "BSL": {
                # > 08:05
                "T1": datetime.strptime("2019-01-21T08:05", '%Y-%m-%dT%H:%M')
            },
            "ESE": {
                # < 16:25
                "T1": datetime.strptime("2019-01-21T16:25", '%Y-%m-%dT%H:%M')
            },
            "ESL": {
                # 16:35 < ts < 17:00
                "T1": datetime.strptime("2019-01-21T16:35", '%Y-%m-%dT%H:%M'),
                "T2": datetime.strptime("2019-01-21T17:00", '%Y-%m-%dT%H:%M')
            },
            "BBE": [
                {
                    # break is 13:00 - 14:00
                    # 12:30 < ts < 12:55
                    "T1": datetime.strptime("2019-01-21T12:30", '%Y-%m-%dT%H:%M'),
                    "T2": datetime.strptime("2019-01-21T12:55", '%Y-%m-%dT%H:%M')
                }
            ],
            "EBL": [
                {
                    # break is 13:00 - 14:00
                    # 14:05 < ts < 14:30
                    "T1": datetime.strptime("2019-01-21T14:05", '%Y-%m-%dT%H:%M'),
                    "T2": datetime.strptime("2019-01-21T14:30", '%Y-%m-%dT%H:%M')
                }
            ],
            "SIU": {
                # > 17:00
                "T1": datetime.strptime("2019-01-21T17:00", '%Y-%m-%dT%H:%M')
            },
            "SOU": {
                # < 16:25 (shift end is 16:30)
                "T1": datetime.strptime("2019-01-21T16:25", '%Y-%m-%dT%H:%M')
            },
            "WOB": [
                {
                    # break is 13:00 - 14:00
                    # 13:05 < ts < 13:55
                    "T1": datetime.strptime("2019-01-21T13:05", '%Y-%m-%dT%H:%M'),
                    "T2": datetime.strptime("2019-01-21T13:55", '%Y-%m-%dT%H:%M')
                }
            ],
        }
    }
}

# bse = BSE(schedule)
# bse_events1 = create_event("LOGIN", "P0001", "2019-01-21T07:33:00.012Z")
# bse_events2 = create_event("HEART_BEAT", "P0001", "2019-01-21T07:55:00.012Z")
# bse.process(bse_events1, "P0001", False)
# bse.process(bse_events2, "P0001", True)

# bsl = BSL(schedule)
# bsl_events1 = create_event("LOGIN", "P0001", "2019-01-21T08:06:00.012Z")
# bsl_events2 = create_event("HEART_BEAT", "P0001", "2019-01-21T16:32:00.012Z")
# bsl.process(bsl_events1, "P0001", False)
# bsl.process(bsl_events2, "P0001", True)

# ese = ESE(schedule)
# ese_events1 = create_event("LOGOUT", "P0001", "2019-01-21T16:20:00.012Z")
# ese.process(ese_events1, "P0001", False)

# esl = ESL(schedule)
# esl_events1 = create_event("HEART_BEAT", "P0001", 
#                            "2019-01-21T16:36:00.012Z", "Available")
# esl.process(esl_events1, "P0001", False)

# bbe = BBE(schedule)
# bbe_events1 = create_event("HEART_BEAT", "P0001",
#                            "2019-01-21T12:40:00.012Z", "Offline")
# bbe.process(bbe_events1, "P0001", False)

# ebl = EBL(schedule)
# ebl_events1 = create_event("HEART_BEAT", "P0001",
#                            "2019-01-21T14:25:00.012Z", "Offline")
# ebl.process(ebl_events1, "P0001", False)

# siu = SIU(schedule)
# siu_events1 = create_event("HEART_BEAT", "P0001",
#                            "2019-01-21T17:05:00.012Z", "Available")
# siu.process(siu_events1, "P0001", False)

# sou = SOU(schedule)
# sou_events1 = create_event("LOGOUT", "P0001",
#                            "2019-01-21T16:20:00.012Z", "Offline")
# sou_events2 = create_event("LOGIN", "P0001",
#                            "2019-01-21T16:20:20.012Z", "Offline")
# sou_events3 = create_event("HEART_BEAT", "P0001",
#                            "2019-01-21T16:31:00.012Z", "Offline")
# sou.process(sou_events1, "P0001", False)
# sou.process(sou_events2, "P0001", True)
# sou.process(sou_events3, "P0001", True)

# wob = WOB(schedule)
# wob_events1 = create_event("HEART_BEAT", "P0001",
#                            "2019-01-21T13:16:00.012Z", "Available")
# wob.process(wob_events1, "P0001", False)
