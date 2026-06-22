from nba_api.stats.static import teams
import json

all_teams = teams.get_teams()

with open("../raw_data/games/raw_data/all_teams.json", "w") as f:
    json.dump(all_teams, f, indent=4)