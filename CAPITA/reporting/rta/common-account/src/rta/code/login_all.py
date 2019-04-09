from datetime import datetime
from datetime import timedelta
from db import DbTable


alarm_tablename = "rta-alarmsdb-ccm-test"
active_alarms = DbTable(alarm_tablename)
history_tablename = "rta-eventhistory-ccm-test"
history = DbTable(history_tablename)

print(active_alarms.items[0])
history_updates = []

for alarm in active_alarms.items:
    username = alarm.get("username")
    alarmcode = alarm.get("alarmcode")

    now = datetime.now()
    now12 = now + timedelta(hours=12)

    print(f"username={username}, alarmcode={alarmcode}")
    if username and alarmcode == "BSL":
        history_updates.append({
            "type": "put",
            "item": {
                "username": username,
                "prop": "LOGIN",
                "ts": now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "ttl": int(now12.timestamp())
            }
        })

print(f"Updates:\n{history_updates}")
history.run_updates(history_updates)

alarm_updates = []
for update in history_updates:
    alarm_updates.append({
        "type": "delete",
        "key": {
            "alarmcode": "BSL",
            "username": update.get("item", {}).get("username")
        }
    })

active_alarms.run_updates(alarm_updates)
