from nba_api.stats.static import players
import json



all_players = players.get_players()

with open("../raw_data/games/raw_data/all_players.json", "w") as f:
    json.dump(all_players, f, indent=4)