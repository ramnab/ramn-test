from datetime import datetime
import json


class Event(object):

    def __init__(self, data):
        self._data = data
        if data.get("EventTimestamp"):
            self.timestamp = data.get("EventTimestamp")
            self.ts = datetime.strptime(data.get("EventTimestamp"), '%Y-%m-%dT%H:%M:%S')
            self.username = data.get("Configuration", {}).get("Username")

        self.type = data.get("EventType")

    def __lt__(self, other):
        if isinstance(other, datetime):
            print(f"{self.ts} < {other}")
            return self.ts < other
        elif isinstance(other, Event):
            print(f"{self.ts} < {other.ts}")
            return self.ts < other.ts

    def __gt__(self, other):
        if isinstance(other, datetime):
            print(f"{self.ts} > {other}")
            return self.ts > other
        elif isinstance(other, Event):
            print(f"{self.ts} > {other.ts}")
            return self.ts > other.ts

    def __str__(self):
        if self._data:
            return json.dumps(self._data)
        return "{}"


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
