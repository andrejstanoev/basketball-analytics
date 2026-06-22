import os.path
import time
import json
import pandas as pd
from nba_api.stats.endpoints import commonplayerinfo

all_players = pd.read_json("../raw_data/all_players.json")

players_ids = all_players["id"].tolist()

for id in players_ids:

    filename = f"../raw_data/individual_player_info/player_{id}.json"
    if os.path.exists(filename):
        print(f"⏭️ Skipping {id} already fetched")
        continue
    try:
        print(f"Fetching data for player with id: {id}")
        info = commonplayerinfo.CommonPlayerInfo(player_id=id)
        info_data = json.loads(info.get_normalized_json())

        player_info = info_data["CommonPlayerInfo"][0]

        with open(filename, "w") as f:
            json.dump(player_info, f, indent=4)

        print(f"✅ Saved player {id}")


    except Exception as e:
        print(f"❌ Failed for player with id: {id} ; {e}")

    time.sleep(2)

print("Merging all players into one file...")
all_players = []

for player_id in players_ids:
    filepath = f"../raw_data/individual_player_info/player_{player_id}.json"
    if os.path.exists(filepath):
        with open(filepath) as f:
            all_players.append(json.load(f))

with open("../raw_data/players_info/players_info.json", "w") as f:
    json.dump(all_players, f, indent=4)

print(f"✅ FINISHED! Merged {len(all_players)} players into players_info.json")