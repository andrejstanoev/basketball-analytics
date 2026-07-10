from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import row_number, col, concat, lit, coalesce, trim, when, upper,explode
from constants import BRONZE_DIR, SILVER_DIR
from utils import get_logger

logger = get_logger("player_games.py")

spark = SparkSession.builder.master("local[*]").appName("player_games").getOrCreate()
logger.info("Created spark session called player_games")

data = spark.read.format("json").option("multiline",True).load(f"{BRONZE_DIR}/players_games")
logger.info("Read the data from bronze directory player_games folder")

data_2 = data.select(
    explode(col("PlayerGameLogs")).alias("logs"),
    col("season"),
    col("type")
)

final_data = data_2.select(
    col("logs.*"),
    col("season"),
    col("type")
)
logger.info("Filtered the data")

final_df = final_data.select(
    col("season"),
    col("type"),
    col("PLAYER_ID").alias("player_id"),
    col("GAME_ID").alias("game_id"),
    col("TEAM_ID").alias("team_id"),
    col("GAME_DATE").alias("game_date"),
    col("MIN").alias("minutes"),
    col("PTS").alias("points"),
    col("AST").alias("assists"),
    col("BLK").alias("blocks"),
    col("BLKA").alias("blocks_against"),
    col("DD2").alias("has_double_double"),
    col("TD3").alias("has_triple_double"),
    col("DREB").alias("defensive_rebounds"),
    col("OREB").alias("offensive_rebounds"),
    col("REB").alias("rebounds"),
    col("STL").alias("steals"),
    col("TOV").alias("turnovers"),
    col("FG3A").alias("field_goals_3_attempted"),
    col("FG3M").alias("field_goals_3_made"),
    col("FG3_PCT").alias("field_goals_3_percentage"),
    col("FGA").alias("field_goals_attempted"),
    col("FGM").alias("field_goals_made"),
    col("FG_PCT").alias("field_goals_percentage"),
    col("FTA").alias("free_throws_attempted"),
    col("FTM").alias("free_throws_made"),
    col("FT_PCT").alias("free_throw_percentage"),
    col("PF").alias("personal_fouls"),
    col("PFD").alias("personal_fouls_drawn"),
    col("PLUS_MINUS").alias("plus_minus")
)
logger.info("Selected the columns that i need")

final_data.write.format("parquet").mode("overwrite").save(f"{SILVER_DIR}/player_games")
logger.info("Written the data to the silver layer")

spark.stop()
logger.info("Stopped spark session named player_games")