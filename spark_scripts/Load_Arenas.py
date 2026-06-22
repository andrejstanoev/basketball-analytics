from pyspark.sql.types import *
from pyspark.sql.functions import col, concat, lit,when
from constants import URL, PROPERTIES
from utils import *

spark = create_spark_session("Load_Arenas")

db_arenas_df = spark.read.jdbc(url=URL, table="arena", properties=PROPERTIES)

arena_data = spark.read.format("json").option("multiline", True).load("../raw_data/arena_data/arena_combined.json")
arena_data = arena_data.drop_duplicates(["arenaId", "team_id"]).where(col('arenaId') != 0)


src = arena_data.join(other=db_arenas_df,on=(arena_data["arenaId"] == db_arenas_df["arena_source_id"]) & (arena_data["team_id"] == db_arenas_df["team_source_id"] ),how="leftanti")


final_df = src.select(
                col('arenaCity').alias('arena_city'),
                col('arenaCountry').alias('arena_country'),
                col('arenaId').alias('arena_source_id'),
                col('arenaName').alias('arena_name'),
                col('arenaState').alias('arena_state'),
                col('arenaTimezone').alias('arena_timezone'),
                col('team_id').alias("team_source_id")
            )

if final_df.count() == 0:
    print("No new arenas")
else:
    final_df.write.jdbc(url=URL,table="arena",mode="append",properties=PROPERTIES)

    print(f"NEW ARENAS COUNT: {final_df.count()}")

    print(final_df.show(200))

    print("Successfully loaded arena infos into table Arena")

spark.stop()