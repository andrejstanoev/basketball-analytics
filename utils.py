from pyspark.sql import SparkSession
from constants import *

def create_spark_session(app_name):

    spark = (SparkSession.builder
         .master("local[*]")
         .appName(app_name)
         .config("spark.jars", JAR_FILE_PATH)
         .getOrCreate()
    )
    return spark


def get_all_seasons():
    return [f"{year}-{str(year + 1)[-2:]}" for year in range(1985, 2026)]