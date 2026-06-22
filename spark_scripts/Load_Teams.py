from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col, concat, lit
from constants import URL,PROPERTIES
from utils import create_spark_session

spark = create_spark_session("Load_Arenas")

db_team_df = spark.read.jdbc(url=URL, table="team", properties=PROPERTIES)


team_data = spark.read.format("json").option("multiline", True).load("../raw_data/team_info/all_teams_info.json")

src = team_data.join(other=db_team_df,on=team_data["TEAM_ID"]==db_team_df["team_source_id"],how="leftanti")

final_df = src.select(
    col("TEAM_ID").alias("team_source_id"), #bigint
    col("TEAM_CITY").alias("team_city"),
    col("TEAM_NAME").alias("team_name"),
    concat(col("TEAM_CITY"), lit(" "), col("TEAM_NAME")).alias("full_team_name"),
    col("TEAM_ABBREVIATION").alias("team_abbreviation"),
    col("TEAM_CONFERENCE").alias("conference"),
    col("TEAM_DIVISION").alias("division"),
    col("NICKNAME").alias("nickname"),
    col("YEARFOUNDED").alias("year_founded"),
    col("OWNER").alias("owner"),
    col("GENERALMANAGER").alias("general_manager"),
    col("HEADCOACH").alias("head_coach"),
    col("DLEAGUEAFFILIATION").alias("d_league_affiliation")
)

if final_df.count() == 0:
    print("No new teams")
else:
    final_df.write.jdbc(url=URL,table="team",mode="append",properties=PROPERTIES)

    print(f"NEW TEAMS COUNT: {final_df.count()}")

    print("Successfully loaded team infos into table Team")

spark.stop()