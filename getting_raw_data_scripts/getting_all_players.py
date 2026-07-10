import os, time
from constants import BRONZE_DIR
from utils import get_logger
from nba_api.stats.static import players
import json
from datetime import date

def get_players():
    today_date = date.today()

    all_players = players.get_players()

    logger.info(f"Got the data, total {len(all_players)} players")

    os.makedirs(f"{BRONZE_DIR}/players/ingest_date={today_date}/", exist_ok=True)

    with open(f"{BRONZE_DIR}/players/ingest_date={today_date}/players.json", "w") as f:
        json.dump(all_players, f, indent=4)

    logger.info("Completed the ingestion process for the players")

logger = get_logger("getting_all_players.py")

def run_player_ingestion():

    today_date = date.today()
    file_path = f"{BRONZE_DIR}/players/ingest_date={today_date}/players.json"

    if os.path.exists(file_path):
        logger.warning(f"Data for the teams already ingested for {today_date}, skipping")
    else:
        logger.info("Fetching regular info for all the players")
        try:

            get_players()

        except Exception as e:
            logger.error(f"Error: {repr(e)}")
            logger.error("Not completed the ingestion process for the players")
            logger.warning("Retrying...")
            time.sleep(4)
            for i in range(3):
                logger.info(f"Attempt {i}")
                try:
                    get_players()

                    break
                except Exception as e:
                    logger.error(f"Error: {repr(e)}")

                time.sleep(3)

if __name__ == "__main__":
    run_player_ingestion()


