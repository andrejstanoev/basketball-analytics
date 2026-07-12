from pyspark.sql import SparkSession
from constants import BRONZE_DIR, SILVER_DIR
from pyspark.sql.window import Window
from pyspark.sql.functions import row_number, col, concat, lit, coalesce, trim, when, upper
from pyspark.sql.types import *
from utils import get_logger

def clean_string(column, default="Unknown"):
    return when( column.isNull() | (trim(column) == ""), lit(default) ).otherwise(column)

def teams_transformation():

    logger = get_logger("teams.py")

    spark = SparkSession.builder.master("local[*]").appName("teams").getOrCreate()
    logger.info("Created spark session called teams")

    team_data = spark.read.format("json").option("multiline", True).load(f"{BRONZE_DIR}/teams")
    logger.info("read teams data")

    window_specification_team = Window.partitionBy(team_data["id"]).orderBy(team_data["ingest_date"].desc())
    team_partitioned = team_data.withColumn("row_number",row_number().over(window_specification_team))
    team_latest_df = team_partitioned.filter(team_partitioned["row_number"]==1)
    logger.info("partitioned by ingest date and got the latest team data")
    #-----------------------------------------
    team_details_data = spark.read.format("json").option("multiline", True).load(f"{BRONZE_DIR}/teams_details")
    logger.info("read team details data")

    window_specification_details = Window.partitionBy(team_details_data["TEAM_ID"]).orderBy(team_details_data["ingest_date"].desc())
    team_details_partitioned = team_details_data.withColumn("row_number",row_number().over(window_specification_details))
    team_details_latest_df = team_details_partitioned.filter(team_details_partitioned["row_number"]==1)
    logger.info("partitioned by ingest date and got the latest team details data")

    team_latest_df = team_latest_df.alias("teams")
    team_details_latest_df = team_details_latest_df.alias("details")

    joined = team_latest_df.join(team_details_latest_df, col("teams.id") == col("details.TEAM_ID"),"inner"
    )

    final_df = joined.select(
        col("details.TEAM_ID").cast(LongType()).alias("team_source_id"),
        clean_string(col("details.TEAM_CITY")).alias("team_city"),
        clean_string(col("details.TEAM_NAME")).alias("team_name"),
        concat( coalesce (col("details.TEAM_CITY"), lit("Unknown") ), lit(" "), coalesce( col("details.TEAM_NAME"), lit("Unknown") ) ).alias("full_team_name"),
        upper(clean_string(col("details.TEAM_ABBREVIATION"))).alias("team_abbreviation"),
        clean_string(col("details.TEAM_CONFERENCE")).alias("conference"),
        clean_string(col("details.TEAM_DIVISION")).alias("division"),
        clean_string(col("details.NICKNAME")).alias("nickname"),
        coalesce(col("details.YEARFOUNDED").cast(IntegerType()), lit(0)).alias("year_founded"),
        clean_string(col("details.OWNER")).alias("owner"),
        clean_string(col("details.GENERALMANAGER")).alias("general_manager"),
        clean_string(col("details.HEADCOACH")).alias("head_coach"),
        clean_string(col("details.DLEAGUEAFFILIATION")).alias("d_league_affiliation"),
        clean_string(col("teams.state")).alias("state")
    )

    final_df.write.format("parquet").mode("overwrite").save(f"{SILVER_DIR}/teams")
    logger.info("saved to parquet format")

    spark.stop()
    logger.info("Stopped spark session named teams")

if __name__ == "__main__":
    teams_transformation()