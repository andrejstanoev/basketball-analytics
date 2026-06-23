from constants import URL, PROPERTIES
from utils import create_spark_session, get_all_seasons
import pandas as pd, json

spark = create_spark_session("Load_Game_Data")

seasons = get_all_seasons()

types = {
    'Regular Season': 'regular',
    'Playoffs': 'playoffs'
}

for s in seasons:
    for type, label in types.items():
        with open(f"../raw_data/games/games_{s}_{label}_log.json") as f:
            data = json.load(f)
        df = pd.DataFrame(data["LeagueGameLog"])
        game_ids = df["GAME_ID"].unique().tolist()
