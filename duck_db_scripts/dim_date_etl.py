from constants import DUCK_DB_FILE_PATH
import duckdb
from utils import get_logger

logger = get_logger("dim_date_etl.py")

logger.info("Creating a connection")
connection = duckdb.connect(DUCK_DB_FILE_PATH)
logger.info("Created a connection to the database")

logger.info("Starting process...")
connection.sql("""
INSERT INTO dim_date
SELECT
    CAST(strftime(d, '%Y%m%d') AS INTEGER)                     AS date_key,
    d                                                           AS date,
    CAST(strftime(d, '%Y') AS SMALLINT)                        AS year,
    CAST(quarter(d) AS TINYINT)                                AS quarter,
    CAST(month(d) AS TINYINT)                                  AS month,
    CAST(day(d) AS TINYINT)                                    AS day,
    CAST(isodow(d) AS TINYINT)                                 AS day_of_week,
    CAST(weekofyear(d) AS TINYINT)                             AS week_of_year,
    strftime(d, '%B')                                          AS month_name,
    strftime(d, '%A')                                          AS day_name,
    isodow(d) IN (6, 7)                                        AS is_weekend,

    -- Holidays (same as your MS SQL version)
    CASE
        WHEN month(d) = 1  AND day(d) = 1  THEN true   -- New Year's Day
        WHEN month(d) = 1  AND day(d) = 6  THEN true   -- Epiphany
        WHEN month(d) = 1  AND day(d) = 7  THEN true   -- Orthodox Christmas
        WHEN month(d) = 4  AND day(d) = 20 THEN true   -- Orthodox Easter
        WHEN month(d) = 4  AND day(d) = 21 THEN true   -- Easter Monday
        WHEN month(d) = 5  AND day(d) = 1  THEN true   -- Labor Day
        WHEN month(d) = 5  AND day(d) = 24 THEN true   -- Saints Cyril and Methodius Day
        WHEN month(d) = 8  AND day(d) = 2  THEN true   -- Ilinden Uprising Day
        WHEN month(d) = 9  AND day(d) = 8  THEN true   -- Independence Day
        WHEN month(d) = 10 AND day(d) = 11 THEN true   -- Day of the Macedonian Revolution
        WHEN month(d) = 12 AND day(d) = 8  THEN true   -- Saint Clement of Ohrid Day
        ELSE false
    END                                                        AS is_holiday,

    DATE_TRUNC('year', d)                                      AS first_day_of_year,
    (DATE_TRUNC('year', d) + INTERVAL '1 year' - INTERVAL '1 day') AS last_day_of_year,
    DATE_TRUNC('quarter', d)                                   AS first_day_of_quarter,
    (DATE_TRUNC('quarter', d) + INTERVAL '3 months' - INTERVAL '1 day') AS last_day_of_quarter,

    CASE
        WHEN month(d) BETWEEN 3 AND 5 THEN 'Spring'
        WHEN month(d) BETWEEN 6 AND 8 THEN 'Summer'
        WHEN month(d) BETWEEN 9 AND 11 THEN 'Autumn'
        ELSE 'Winter'
    END                                                        AS season

FROM (
    SELECT
        DATE '1980-01-01' + INTERVAL (i) DAY AS d
    FROM generate_series(0, 22279) AS t(i)  -- 14609 days = 1990-01-01 to 2030-12-31
) dates;
""")
logger.info("Finished process")

logger.info("Closing the connection")
connection.close()
logger.info("Closed the connection")