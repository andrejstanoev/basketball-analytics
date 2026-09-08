from constants import DUCK_DB_FILE_PATH
import duckdb
from utils import get_logger

logger = get_logger("creating_fact_tables.py")

logger.info("Creating a connection")
connection = duckdb.connect(DUCK_DB_FILE_PATH)
logger.info("Created a connection to the database")

logger.info("Creating sequence for Skey and table fact_player_games")
#transactional fact table
connection.sql("""
create sequence if not exists skey_fact_player_games start 1;
create table if not exists fact_player_games(
       Skey bigint primary key default nextval('skey_fact_player_games'),
       season varchar,
       type varchar,
       player_skey bigint,
       game_skey bigint,
       team_skey bigint,
       game_date date,
       minutes int,
       points int,
       assists int,
       blocks int,
       blocks_against int,
       has_double_double boolean,
       has_triple_double boolean,
       defensive_rebounds int,
       offensive_rebounds int,
       rebounds int,
       steals int,
       turnovers int,
       field_goals_3_attempted int,
       field_goals_3_made int,
       field_goals_3_percentage decimal(19,2),
       field_goals_attempted int,
       field_goals_made int,
       field_goals_percentage decimal(19,2),
       free_throws_attempted int,
       free_throws_made int,
       free_throw_percentage decimal(19,2),
       personal_fouls int,
       personal_fouls_drawn int,
       plus_minus int,
       ETL_LoadTime timestamp default now()
);
""")
logger.info("Created sequence and table fact_player_games")


logger.info("Creating sequence for Skey and table fact_team_games")
#transactional fact table
connection.sql("""
create sequence if not exists skey_fact_team_games start 1;

create table fact_team_games(
       Skey bigint primary key default nextval('skey_fact_team_games'),
       season varchar,
       type varchar,
       team_skey bigint,
       game_skey bigint,
       game_date date,
       win_loss varchar,
       minutes int,
       points int,
       assists int,
       defensive_rebounds int,
       offensive_rebounds int,
       rebounds int,
       blocks int,
       field_goals_3_attempted int,
       field_goals_3_made int,
       field_goals_3_percentage decimal(19,2),
       field_goals_attempted int,
       field_goals_made int,
       field_goals_percentage decimal(19,2),
       free_throws_attempted int,
       free_throws_made int,
       free_throw_percentage decimal(19,2),
       personal_fouls int,
       steals int,
       turnovers int,
       plus_minus int,
       ETL_LoadTime timestamp default now()
);
""")
logger.info("Created sequence and table fact_team_games")



logger.info("Closing the connection")
connection.close()
logger.info("Closed the connection")