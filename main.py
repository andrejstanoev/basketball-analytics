from utils import get_logger
from getting_raw_data_scripts.getting_all_players import run_player_ingestion
from getting_raw_data_scripts.getting_all_teams import run_team_ingestion
from getting_raw_data_scripts.getting_players_info import run_player_info_ingestion
from getting_raw_data_scripts.getting_team_details import run_team_details_ingestion
from getting_raw_data_scripts.getting_all_games import run_games_ingestion
from getting_raw_data_scripts.getting_all_games_players import run_games_players_ingestion


logger = get_logger("main.py")

logger.info("Starting the whole process")

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
#run_player_info_ingestion()
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


logger.info("All the processes finished")