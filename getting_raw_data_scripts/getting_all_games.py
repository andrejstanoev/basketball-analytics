from nba_api.stats.endpoints import leaguegamelog
import json, time, os
from utils import get_all_seasons

os.makedirs("../raw_data/games", exist_ok=True)

# start = 1900
# seasons = []
# for num in range(85, 96):
#     season = start + num
#     season_string = f"{season}-{str(num+1).zfill(2)}"
#     seasons.append(season_string)

seasons = get_all_seasons()

season_types = {
    'Regular Season': 'regular',
    'Playoffs': 'playoffs'
}

for s in seasons:
    for season_type, label in season_types.items():

        if os.path.exists(f"../raw_data/games/games_{s}_{label}_log.json"):
            print(f"⏭️ Skipping, games already fetched for season {s}")
            continue

        try:
            print(f"Fetching {s} {season_type}...")

            games = leaguegamelog.LeagueGameLog(
                season=s,
                season_type_all_star=season_type
            )
            data = json.loads(games.get_normalized_json())

            filename = f"../raw_data/games/games_{s}_{label}_log.json"
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)

            print(f"✅ Saved {filename}")

        except Exception as e:
            print(f"❌ Failed {s} {season_type}: {e}")

        time.sleep(4)