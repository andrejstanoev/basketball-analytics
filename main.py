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

logger = get_logger("main.py")

logger.info("Starting the whole process")

#=========================BRONZE LAYER===========================================================

# 1
#============================================================

logger.info("Starting the player ingestion")
run_player_ingestion()
logger.info("Finished the player ingestion")

# 2
#============================================================

logger.info("Starting the team ingestion")
run_team_ingestion()
logger.info("Finished the team ingestion")

#3
#============================================================

logger.info("Starting the player info ingestion")
run_player_info_ingestion()
logger.info("Finished the player info ingestion")

#4
#============================================================

logger.info("Starting the team details ingestion")
run_team_details_ingestion()
logger.info("Finished the team details ingestion")

#5
#============================================================
logger.info("Starting the games ingestion")
run_games_ingestion()
logger.info("Finished the game ingestion")

#6
#============================================================
logger.info("Starting the games_players ingestion")
run_games_players_ingestion()
logger.info("Finished the games_players ingestion")

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