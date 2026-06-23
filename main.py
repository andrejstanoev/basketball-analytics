from utils import get_logger
from getting_raw_data_scripts.getting_all_players import run_player_ingestion
from getting_raw_data_scripts.getting_all_teams import run_team_ingestion
logger = get_logger("main.py")

logger.info("Starting the whole process")

run_player_ingestion()
run_team_ingestion()

logger.info("All the processes finished")