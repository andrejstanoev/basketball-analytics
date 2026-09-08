from constants import DUCK_DB_FILE_PATH
import duckdb
from utils import get_logger

logger = get_logger("creating_dimensions.py")

logger.info("Creating a connection")
connection = duckdb.connect(DUCK_DB_FILE_PATH)
logger.info("Created a connection to the database")

logger.info("Creating sequence for Skey and dimension player")
connection.sql("""
create sequence if not exists skey_dim_player start 1;

create table if not exists dim_player(
    SKey bigint primary key default nextval('skey_dim_player'),
    player_id bigint,
    full_name varchar,
    birthdate date,
    is_active boolean,
    height varchar,
    weight decimal(19,2),
    season_experience int,
    position varchar,
    draft_year varchar,
    draft_number varchar,
    school varchar,
    country varchar,
    SCD_KeyHash varchar,
    SCD_ColumnHash varchar,
    SCD_ValidFrom timestamp,
    SCD_ValidTo timestamp default '9999-12-31'::timestamp,
    SCD_IsCurrent boolean not null,
    SCD_FirstKey int,
    ETL_LoadTime timestamp default now()
);
""")
logger.info("Created sequence and player dimension")

logger.info("Creating sequence for Skey and team dimension")
connection.sql("""

create sequence if not exists skey_dim_teams start 1;

create table if not exists dim_team(
    SKey bigint primary key default nextval('skey_dim_teams'),
    team_id bigint,
    team_city varchar,
    team_name varchar,
    full_team_name varchar,
    team_abbreviation varchar,
    conference varchar,
    division varchar,
    nickname varchar,
    year_founded int,
    owner varchar,
    general_manager varchar,
    head_coach varchar,
    d_league_affiliation varchar,
    state varchar,
    SCD_KeyHash varchar,
    SCD_ColumnHash varchar,
    SCD_ValidFrom timestamp,
    SCD_ValidTo timestamp default '9999-12-31'::timestamp,
    SCD_IsCurrent boolean not null,
    SCD_FirstKey int,
    ETL_LoadTime timestamp default now()
);
""")
logger.info("Created sequence and team dimension")

logger.info("Creating sequence for Sket and game dimension")
connection.sql("""
create sequence if not exists skey_dim_games start 1;

create table if not exists dim_game(
    SKey bigint primary key default nextval('skey_dim_games'),
    game_id bigint,
    home_team_id bigint,
    home_team_name varchar,
    away_team_id bigint,
    away_team_name varchar,
    winner_team_id bigint,
    winner_team_name varchar,
    loser_team_id bigint,
    loser_team_name varchar,
    season varchar,
    game_date date,
    game_type varchar,
    ETL_LoadTime timestamp default now()
);
""")
logger.info("Created sequence and game dimension")

logger.info("Creating sequence for Skey and date dimension")
connection.sql("""
CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,
    date            DATE NOT NULL,
    year            SMALLINT NOT NULL,
    quarter         TINYINT NOT NULL,
    month           TINYINT NOT NULL,
    day             TINYINT NOT NULL,
    day_of_week     TINYINT NOT NULL,
    week_of_year    TINYINT NOT NULL,
    month_name      VARCHAR(20) NOT NULL,
    day_name        VARCHAR(20) NOT NULL,
    is_weekend      BOOLEAN NOT NULL,
    is_holiday      BOOLEAN NOT NULL,
    first_day_of_year   DATE NOT NULL,
    last_day_of_year    DATE NOT NULL,
    first_day_of_quarter DATE NOT NULL,
    last_day_of_quarter  DATE NOT NULL,
    season          VARCHAR(20) NOT NULL
);
""")
logger.info("Created sequence and date dimension")


logger.info("Closing the connection")
connection.close()
logger.info("Closed the connection")