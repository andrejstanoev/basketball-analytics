import time
import glob
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col,explode
from nba_api.stats.endpoints import boxscoresummaryv3

spark = SparkSession.builder.master("local[*]").appName("Get_Arenas").getOrCreate()

df_games = spark.read.format("json").option("multiline",True).load("../raw_data/games/games_*_regular_log.json")
df_games = df_games.select(explode("LeagueGameLog").alias("game"))
df_games = df_games.select('game.*')

wtf = df_games.where(col("MATCHUP").contains("vs")).select(col("GAME_ID"),col("SEASON_ID"),col("TEAM_ID")).collect()

list_structs = []
for r in wtf:
    list_structs.append({
        "game_id":r["GAME_ID"],
        "season_id" : r["SEASON_ID"],
        "team_id" : r["TEAM_ID"]
    })

season_team_map = {

}

for item in list_structs:
    season_id = item["season_id"]
    team_id = item["team_id"]
    game_id = item["game_id"]
    if f"{season_id};{team_id}" in season_team_map:
        print(f"⏭️ Skipping {season_id} - {team_id} already fetched")
        continue
    try:
        print(f"Fetching data for {season_id} - {team_id}")

        df = boxscoresummaryv3.BoxScoreSummaryV3(game_id=game_id).get_data_frames()
        df_arena_stats = df[2]
        df_arena_stats["team_id"] = team_id
        df_arena_stats.to_json(f"../raw_data/arena_data/arena_{season_id}-{team_id}.json",orient="records", indent=4)
        season_team_map[f"{season_id};{team_id}"] = True

        print(f"✅ Saved {season_id} - {team_id}")

    except Exception as e:
        print(f"❌ Failed for game with id: {game_id} ; {e}")

    time.sleep(2)


all_data = []
files = glob.glob("../raw_data/arena_data/arena_*.json")

for file in files:
    with open(file) as f:
        data = json.load(f)
        if isinstance(data, list):
            all_data.extend(data)
        else:
            all_data.append(data)

with open("../raw_data/arena_data/arena_combined.json", "w") as f:
    json.dump(all_data, f, indent=4)

print(f"Combined {len(files)} files into one, total records: {len(all_data)}")

spark.stop()
