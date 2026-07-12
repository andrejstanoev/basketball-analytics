from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import row_number, col, concat, lit, coalesce, trim, when, upper,explode
from constants import BRONZE_DIR, SILVER_DIR
from utils import get_logger
import os

def teams_games_transformation():

    logger = get_logger("teams_games.py")

    spark = SparkSession.builder.master("local[*]").appName("teams_games").getOrCreate()
    logger.info("Created spark session called teams_games")

    data = spark.read.format("json").option("multiline",True).load(f"{BRONZE_DIR}/games")
    logger.info("Read the data from bronze directory games folder")

    data_2 = data.select(
        explode( col("LeagueGameLog") ).alias("logs"),
        col("season"),
        col("type")
    )

    final_data = data_2.select(
        col("logs.*"),
        col("season"),
        col("type")
    )
    logger.info("Destructured the data")

    final_df = final_data.select(
        col("season"),
        col("type"),
        col("TEAM_ID").alias("team_id"),
        col("GAME_ID").alias("game_id"),
        col("WL").alias("win_loss"),
        col("MIN").alias("minutes"),
        col("PTS").alias("points"),
        col("AST").alias("assists"),
        col("DREB").alias("defensive_rebounds"),
        col("OREB").alias("offensive_rebounds"),
        col("REB").alias("rebounds"),
        col("BLK").alias("blocks"),
        col("FG3A").alias("field_goals_3_attempted"),
        col("FG3M").alias("field_goals_3_made"),
        col("FG3_PCT").alias("field_goal_3_percentage"),
        col("FGA").alias("field_goals_attempted"),
        col("FGM").alias("field_goals_made"),
        col("FG_PCT").alias("field_goal_percentage"),
        col("FTA").alias("free_throws_attempted"),
        col("FTM").alias("free_throws_made"),
        col("FT_PCT").alias("free_throw_percentage"),
        col("PF").alias("personal_fouls"),
        col("STL").alias("steals"),
        col("TOV").alias("turnovers"),
        col("PLUS_MINUS").alias("plus_minus")
    )
    logger.info("Selected the columns that i need")

    os.makedirs(f"{SILVER_DIR}/teams_games", exist_ok=True )

    final_df.write.format("parquet").mode("overwrite").save(f"{SILVER_DIR}/teams_games")
    logger.info("Written the data to the silver layer")

    spark.stop()
    logger.info("Stopped spark session named teams_games")

if __name__ == "__main__":
    teams_games_transformation()