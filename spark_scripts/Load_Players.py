from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import col
from constants import URL, PROPERTIES
from utils import create_spark_session


spark = create_spark_session("Load_Players")

db_players_df = spark.read.jdbc(url=URL, table="player", properties=PROPERTIES)

df_1 = spark.read.format("json").option("multiline", True).option("path","../raw_data/players_info/players_info.json").load()
df_2 = spark.read.format("json").option("multiline", True).option("path","../raw_data/all_players.json").load()

joined = df_1.join(other=df_2, on=df_1.PERSON_ID==df_2.id, how="inner")

src = joined.join(other=db_players_df,on=joined["id"] == db_players_df["source_player_id"],how="leftanti")


final_df = src.select(col("id").alias("source_player_id"),
              col("full_name"),
              col("BIRTHDATE").try_cast(DateType()).alias("birthdate"),
              col("is_active").alias("is_active"),
              col("HEIGHT").alias("height"),
              col("WEIGHT").try_cast(IntegerType()).alias("weight"),
              col("SEASON_EXP").alias("season_experience"),
              col("POSITION").alias("position"),
              col("FROM_YEAR").try_cast(StringType()).alias("from_year"),
              col("TO_YEAR").try_cast(StringType()).alias("to_year"),
              col("DRAFT_YEAR").try_cast(StringType()).alias("draft_year"),
              col("DRAFT_ROUND").try_cast(StringType()).alias("draft_round"),
              col("DRAFT_NUMBER").try_cast(StringType()).alias("draft_number"),
              col("SCHOOL").alias("school"),
              col("COUNTRY").alias("country")
              )

if final_df.count() == 0:
    print("No new players")
else:
    final_df.write.jdbc(url=URL,table="player",mode="append",properties=PROPERTIES)

    print(f"NEW PLAYERS COUNT: {final_df.count()}")

    print("Successfully loaded player infos into table Player")

spark.stop()
