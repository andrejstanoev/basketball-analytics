from pyspark.sql import SparkSession
from constants import *
import logging
import colorlog

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


def get_logger(name):
    handler = colorlog.StreamHandler()

    formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    handler.setFormatter(formatter)

    logger = colorlog.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger