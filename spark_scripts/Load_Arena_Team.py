from pyspark.sql.types import *
from pyspark.sql.functions import col, concat, lit,when
from constants import *
from utils import *

spark = create_spark_session("Load_Arena_Team")

db_team_df = spark.read.jdbc(url=URL,table="team",properties=PROPERTIES)

db_arena_df = spark.read.jdbc(url=URL,table="arena", properties=PROPERTIES)

joined = db_team_df.join(other=db_arena_df,on = "team_source_id",how="inner")

arena_info_df = spark.read.format("json").option("multiline",True).load("../raw_data/team_info/all_teams_info.json")

res = joined.join(other=arena_info_df,on=(joined["team_source_id"] == arena_info_df["TEAM_ID"]) & (joined["arena_name"] == arena_info_df["ARENA"]),how="left" )

res = res.drop(arena_info_df["TEAM_ID"])


final_df = res.select(
    col("team_id"),
    col("arena_id"),
    col("full_team_name"),
    col("arena_name"),
    when(col("TEAM_CODE").isNull(), False).otherwise(True).alias("is_current")
)

final_df.write.jdbc(url=URL,table="team_arena",mode="append",properties=PROPERTIES)


spark.stop()