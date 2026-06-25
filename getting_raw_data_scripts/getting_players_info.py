
import os.path, time, json, pandas as pd

from requests import ReadTimeout

from utils import get_logger
from nba_api.stats.endpoints import commonplayerinfo
from datetime import date
from constants import BRONZE_DIR


logger = get_logger("getting_player_info.py")

def fetch_player_with_retry(player_id, retries):
    for attempt in range(retries):
        try:
            info = commonplayerinfo.CommonPlayerInfo(
                player_id=player_id,
                timeout=60
            )
            return info
        except ReadTimeout:
            wait = 10 * (attempt + 1)
            logger.warning(f"Timeout for {player_id}, attempt {attempt+1}, waiting {wait}s")
            time.sleep(wait)
    return None

def extract_player_info(info):
    info_data = json.loads(info.get_normalized_json())
    return info_data["CommonPlayerInfo"][0]

def run_player_info_ingestion():
    today_date = date.today()

    file_path = f"{BRONZE_DIR}/players_info/ingest_date={today_date}/players_info.json"

    if os.path.exists(file_path):
        logger.warning(f"Data for the players already ingested for {today_date}, skipping")
    else:
        players_path_file = f"{BRONZE_DIR}/players/ingest_date={today_date}/players.json"
        all_players = pd.read_json(players_path_file)
        players_ids = all_players["id"].tolist()

        json_list = []

        for id in players_ids:
            try:
                logger.info(f"Fetching extra information for player with id={id}")
                info = commonplayerinfo.CommonPlayerInfo(player_id=id)
                player_info = extract_player_info(info)

                json_list.append(player_info)
                logger.info(f"Got the extra information for player with id={id}")

            except (ReadTimeout, ConnectionError) as e:
                logger.warning(f"Timeout for player {id}, retrying. Error: {repr(e)}")
                info = fetch_player_with_retry(id,3)
                if info is not None:
                    player_info = extract_player_info(info)
                    json_list.append(player_info)
                    logger.info(f"Got the extra information for player with id={id}")
                else:
                    logger.error(f"Failed to fetch info for player with id={id}")

            except Exception as e:
                logger.error(f"Error for player with id={id} : {repr(e)}")

            time.sleep(2)

        os.makedirs(f"{BRONZE_DIR}/players_info/ingest_date={today_date}/", exist_ok=True)

        with open(f"{BRONZE_DIR}/players_info/ingest_date={today_date}/players_info.json", "w") as f:
            json.dump(json_list,f,indent=4)

        logger.info("Completed the ingestion process for the players extra information")

if __name__ == "__main__":
    run_player_info_ingestion()