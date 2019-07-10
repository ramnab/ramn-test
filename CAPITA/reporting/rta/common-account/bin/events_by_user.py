import json
import sys
import os

agents = {}
results_dir = sys.argv[1]

for f in sys.argv[2::]:
    print(f"Reading file: {f}")
    with open(f) as j:
        fstr = j.read()
        if "}{" in fstr:
            fstr = "[" + fstr.replace("}{", "}, {") + "]"

        data = json.loads(fstr)
        for datum in data:
            agent_id = datum.get("CurrentAgentSnapshot", {}) \
                      .get("Configuration", {}) \
                      .get("Username")

            if agent_id and "@" not in agent_id:
                if not agents.get(agent_id):
                    agents[agent_id] = []
                agents.get(agent_id).append(datum)

for agent_id, events in agents.items():
    try:
        print(f"Processing agent {agent_id}")
        if not os.path.exists(f'{results_dir}{agent_id}'):
            os.makedirs(f'{results_dir}{agent_id}')
        with open(f'{results_dir}{agent_id}/agent_events.json', 'w') as f:
            f.write(json.dumps(events))
    except Exception as e:
        print(f"Unable to write for agent id {agent_id}")
