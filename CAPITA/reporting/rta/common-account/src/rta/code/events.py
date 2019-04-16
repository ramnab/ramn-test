from datetime import datetime
import json
import re


class Event(object):

    def __init__(self, data):
        self._data = data
        event_timestamp = data.get("EventTimestamp")

        if not event_timestamp:
            raise EventException("No EventTimestamp found in data")

        timestamp_match = re.match(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)', event_timestamp)
        if timestamp_match:
            self.timestamp = timestamp_match.group()
            self.ts = datetime.strptime(timestamp_match.group(), '%Y-%m-%dT%H:%M:%S')
        else:
            raise EventException(f"Event timestamp doesn't match pattern: {event_timestamp}")

        self.username = data.get("Configuration", {}).get("Username")
        self.type = data.get("EventType")

    def __lt__(self, other):
        if isinstance(other, datetime):
            return self.ts < other
        elif isinstance(other, Event):
            return self.ts < other.ts

    def __gt__(self, other):
        if isinstance(other, datetime):
            return self.ts > other
        elif isinstance(other, Event):
            return self.ts > other.ts

    def __str__(self):
        if self._data:
            return json.dumps(self._data)
        return "{}"


class EventException(Exception):
    pass


class Events(object):

    def __init__(self, data: list = []):
        self._events = []
        if data:
            for entry in data:
                self._events.append(Event(entry))

    def __add__(self, data):
        if isinstance(data, Event):
            self._events.append(data)
        elif isinstance(data, dict):
            self._events.append(Event(data))

    def filter(self, typs):
        filtered = Events()
        if isinstance(typs, str):
            typs = [typs]

        for event in self._events:
            if event.type in typs:
                filtered + event
        return filtered

    def username(self, usr):
        filtered = Events()
        for event in self._events:
            if event.username == usr:
                filtered + event
        return filtered

    def sort(self, **kwargs):
        if self._events:
            sorted_events = Events()
            reverse = kwargs.get("reverse", False)
            sorted_events._events = sorted(self._events, key=lambda x: x.ts, reverse=reverse)
            return sorted_events
        return self

    @property
    def first(self):
        if self._events:
            return self._events[0]
        return None

    @property
    def usernames(self):
        return [ev.username for ev in self._events]
