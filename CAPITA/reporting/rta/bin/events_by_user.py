import json
import sys
import os

agents = {}
results_dir = sys.argv[1] # e.g. '/mnt/c/Users/ChurcheG/Downloads/capita-connect/tradeuk3-agents/'

for f in sys.argv[2::]:
    print(f"Reading file: {f}")
    with open(f) as j:
        str = j.read()
        if "}{" in str:
            str = "[" + str.replace("}{", "}, {") + "]"

        data = json.loads(str)
        for datum in data:
            id = datum.get("CurrentAgentSnapshot", {}) \
                      .get("Configuration", {}) \
                      .get("Username")

            if id and "@" not in id:
                if not agents.get(id):
                    agents[id] = []
                agents.get(id).append(datum)

for id, events in agents.items():
    try:
        print(f"Processing agent {id}")
        if not os.path.exists(f'{results_dir}{id}'):
            os.makedirs(f'{results_dir}{id}')
        with open(f'{results_dir}{id}/agent_events.json', 'w') as f:
            f.write(json.dumps(events))
    except Exception as e:
        print(f"Unable to write for agent id {id}")
