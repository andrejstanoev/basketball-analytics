from utils import get_logger

from getting_raw_data_scripts.getting_all_players import run_player_ingestion
from getting_raw_data_scripts.getting_all_teams import run_team_ingestion
from getting_raw_data_scripts.getting_players_info import run_player_info_ingestion
from getting_raw_data_scripts.getting_team_details import run_team_details_ingestion
from getting_raw_data_scripts.getting_all_games import run_games_ingestion
from getting_raw_data_scripts.getting_all_games_players import run_games_players_ingestion

from spark_scripts.players import players_transformation
from spark_scripts.teams import teams_transformation
from spark_scripts.games import games_transformation
from spark_scripts.teams_games import teams_games_transformation
from spark_scripts.player_games import player_games_transformation

from duck_db_scripts.creating_dimensions import create_dimensions
from duck_db_scripts.creating_fact_tables import create_fact_tables
from duck_db_scripts.dim_game_etl import dim_game_etl_process
from duck_db_scripts.dim_date_etl import dim_date_etl_process
from duck_db_scripts.dim_player_etl import dim_player_etl_process
from duck_db_scripts.dim_team_etl import dim_team_etl_process
from duck_db_scripts.fact_player_games_etl import fact_player_games_etl_process
from duck_db_scripts.fact_team_games_etl import fact_team_games_etl_process

logger = get_logger("main.py")

logger.info("Starting the whole process")

#=========================BRONZE LAYER===========================================================
#
# # 1
# #============================================================
#
# logger.info("Starting the player ingestion")
# run_player_ingestion()
# logger.info("Finished the player ingestion")
#
# # 2
# #============================================================
#
# logger.info("Starting the team ingestion")
# run_team_ingestion()
# logger.info("Finished the team ingestion")
#
# #3
# #============================================================
#
# logger.info("Starting the player info ingestion")
# run_player_info_ingestion()
# logger.info("Finished the player info ingestion")
#
# #4
# #============================================================
#
# logger.info("Starting the team details ingestion")
# run_team_details_ingestion()
# logger.info("Finished the team details ingestion")
#
# #5
# #============================================================
# logger.info("Starting the games ingestion")
# run_games_ingestion()
# logger.info("Finished the game ingestion")
#
# #6
# #============================================================
# logger.info("Starting the games_players ingestion")
# run_games_players_ingestion()
# logger.info("Finished the games_players ingestion")

#====================================SILVER LAYER=======================================================

#1
#=================================================================
logger.info("Starting players transformation")
players_transformation()
logger.info("Finished players transformation")

#2
#=================================================================
logger.info("Starting teams transformation")
teams_transformation()
logger.info("Finished teams transformation")

#3
#=================================================================
logger.info("Starting games transformation")
games_transformation()
logger.info("Finished games transformation")

#4
#=================================================================
logger.info("Starting teams_games transformation")
teams_games_transformation()
logger.info("Finished teams_games transformation")

#5
#=================================================================
logger.info("Starting player_games transformation")
player_games_transformation()
logger.info("Finished player_games transformation")

logger.info("All the processes finished")

#==============================================GOLD LAYER===============================================

#1
#=================================================================
logger.info("Starting creating dimensions")
create_dimensions()
logger.info("Finished creating dimensions")

#2
#=================================================================
logger.info("Starting creating fact tables")
create_fact_tables()
logger.info("Finished creating fact tables")

#3
#=================================================================
logger.info("Starting date dimension etl process")
dim_date_etl_process()
logger.info("Finished date dimension etl process")

#4
#=================================================================
logger.info("Starting game dimension etl process")
dim_game_etl_process()
logger.info("Finished game dimension etl process")

#5
#=================================================================
logger.info("Starting player dimension etl process")
dim_player_etl_process()
logger.info("Finished player dimension etl process")

#6
#=================================================================
logger.info("Starting team dimension etl process")
dim_team_etl_process()
logger.info("Finished team dimension etl process")

#7
#=================================================================
logger.info("Starting player games fact table etl process")
fact_player_games_etl_process()
logger.info("Finished player games fact table etl process")

#8
#=================================================================
logger.info("Starting team games fact table etl process")
fact_team_games_etl_process()
logger.info("Finished team games fact table etl process")
