from pyspark.sql import SparkSession, DataFrame
from constants import BRONZE_DIR, SILVER_DIR
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col, concat, lit, coalesce, trim, when, upper
from pyspark.sql.types import *
from utils import clean_string, get_logger, clean_integer

def players_transformation():

    logger = get_logger("players.py")

    spark = SparkSession.builder.master("local[*]").appName("players").getOrCreate()
    logger.info("Created spark session called players")

    player_data = spark.read.format("json").option("multiline",True).load(f"{BRONZE_DIR}/players")
    logger.info("read player data")

    window_specification_player = Window.partitionBy(player_data["id"]).orderBy(player_data["ingest_date"].desc())
    player_partitioned = player_data.withColumn("row_number", row_number().over(window_specification_player))
    player_latest : DataFrame = player_partitioned.filter(player_partitioned["row_number"]==1)
    logger.info("partitioned by ingest date and got the latest player data")

    #------------------------------------------

    player_info_data = spark.read.format("json").option("multiline",True).load(f"{BRONZE_DIR}/players_info")
    logger.info("read player extra info data")

    window_specification_player_info = Window.partitionBy(player_info_data["PERSON_ID"]).orderBy(player_info_data["ingest_date"].desc())
    player_info_partitioned = player_info_data.withColumn("row_number",row_number().over(window_specification_player_info))
    player_info_latest : DataFrame = player_info_partitioned.filter( player_info_partitioned["row_number"]==1 )
    logger.info("partitioned by ingest date and got the latest player extra info data")


    joined = player_latest.join(player_info_latest, player_latest["id"]==player_info_latest["PERSON_ID"], "left")


    final_df = joined.select(
        col("id").cast(LongType()).alias("player_source_id"),
        col("full_name").alias("full_name"),
        col("BIRTHDATE").cast(DateType()).alias("birthdate"),
        col("is_active"),
        clean_string(col("HEIGHT")).alias("height"), #some "" values
        when( trim( col("WEIGHT") )=="", 0 ).otherwise(col("WEIGHT").cast(DoubleType())).alias("weight"),
        clean_integer(col("SEASON_EXP")).alias("season_experience"),
        clean_string(col("POSITION")).alias("position"),
        clean_integer(col("FROM_YEAR")).alias("from_year"),
        clean_integer(col("TO_YEAR")).alias("to_year"),
        clean_string(col("DRAFT_YEAR")).alias("draft_year"),
        clean_string(col("DRAFT_ROUND")).alias("draft_round"),
        clean_string(col("DRAFT_NUMBER")).alias("draft_number"),
        clean_string(col("SCHOOL")).alias("school"),
        clean_string(col("COUNTRY")).alias("country")
    )

    final_df.write.format("parquet").mode("overwrite").save(f"{SILVER_DIR}/players")
    logger.info("saved to parquet format")

    spark.stop()
    logger.info("Stopped spark session named players")


if __name__ == "__main__":
    players_transformation()