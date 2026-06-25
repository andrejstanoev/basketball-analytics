import os
from constants import BRONZE_DIR
from utils import get_logger
from nba_api.stats.static import players
import json
from datetime import date
from getting_raw_data_scripts.getting_players_info import run_player_info_ingestion

logger = get_logger("getting_all_players.py")

def run_player_ingestion():

    today_date = date.today()
    file_path = f"{BRONZE_DIR}/players/ingest_date={today_date}/players.json"

    if os.path.exists(file_path):
        logger.warning(f"Data for the teams already ingested for {today_date}, skipping")
    else:
        logger.info("Fetching regular info for all the players")
        try:

            all_players = players.get_players()

            logger.info(f"Got the data, total {len(all_players)} players")

            os.makedirs(f"{BRONZE_DIR}/players/ingest_date={today_date}/", exist_ok=True)

            with open(f"{BRONZE_DIR}/players/ingest_date={today_date}/players.json", "w") as f:
                json.dump(all_players, f, indent=4)

            logger.info("Completed the ingestion process for the players")

            # run_player_info_ingestion(file_path)

        except Exception as e:
            logger.error(f"Error: {repr(e)}")
            logger.error("Not completed the ingestion process for the players")


if __name__ == "__main__":
    run_player_ingestion()


