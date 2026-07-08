from pyspark.sql import SparkSession, DataFrame
from constants import BRONZE_DIR, SILVER_DIR
from pyspark.sql.functions import row_number, col, concat, lit, coalesce, trim, when, upper,explode
from utils import get_logger

logger = get_logger("games.py")

spark = SparkSession.builder.master("local[*]").appName("games").getOrCreate()
logger.info("Create spark session called games")

games_data = spark.read.format("json").option("multiline",True).load(f"{BRONZE_DIR}/games")
logger.info("read games data")

games_2 = games_data.select(
    explode( col("LeagueGameLog") ).alias("games"),
    col("season"),
    col("type")
)

games_df = games_2.select(
    col("games.*"),
    col("season"),
    col("type")
)
logger.info("Transformed game data")


home_games : DataFrame = games_df.filter(col("MATCHUP").contains("vs."))
logger.info("got all home games")

away_games : DataFrame = games_df.filter(col("MATCHUP").contains("@"))
logger.info("got all away games")

joined = home_games.alias("home").join(away_games.alias("away"), home_games["GAME_ID"] == away_games["GAME_ID"], "inner")
logger.info("joined the games")

final_df = joined.select(
    col("home.GAME_ID"),
    col("home.TEAM_ID").alias("home_team_id"),
    col("away.TEAM_ID").alias("away_team_id"),
    col("home.season"),
    col("home.GAME_DATE").alias("game_date"),
    col("home.type")
)

final_df.write.format("parquet").mode("overwrite").save(f"{SILVER_DIR}/games")
logger.info("saved to parquet format")

spark.stop()
logger.info("Stopped spark session named games")