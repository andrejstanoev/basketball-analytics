import asyncio
import os
import time
import json
import pandas as pd
from datetime import date
from requests import ReadTimeout
from nba_api.stats.endpoints import commonplayerinfo
from constants import BRONZE_DIR
from utils import get_logger

logger = get_logger("getting_player_info.py")

def fetch_player_info_sync(player_id, retries=3):

    for attempt in range(retries):
        try:
            info = commonplayerinfo.CommonPlayerInfo(
                player_id=player_id,
                timeout=60
            )
            data = json.loads(info.get_normalized_json())
            return data["CommonPlayerInfo"][0]

        except (ReadTimeout, ConnectionError) as e:
            wait = 10 * (attempt + 1)
            logger.warning(f"Timeout for {player_id}, attempt {attempt+1}/{retries}, waiting {wait}s")
            time.sleep(wait)

        except KeyError as e:
            logger.warning(f"Player {player_id} has no data in NBA system, skipping: {e}")
            return None

        except Exception as e:
            logger.error(f"Error for player {player_id}: {repr(e)}")
            return None

    logger.error(f"All retries failed for player {player_id}")
    return None


async def fetch_player_async(player_id):

    return await asyncio.to_thread(fetch_player_info_sync, player_id)


async def fetch_batch(player_ids_batch):

    tasks = [fetch_player_async(player_id) for player_id in player_ids_batch]
    results = await asyncio.gather(*tasks)
    return results


async def run_ingestion_async(players_ids):

    batch_size = 3
    all_results = []
    total = len(players_ids)

    for i in range(0, total, batch_size):
        batch = players_ids[i:i + batch_size]
        logger.info(f"Processing batch {i//batch_size + 1} — players {i+1} to {min(i+batch_size, total)} of {total}")


        results = await fetch_batch(batch)


        for player_id, result in zip(batch, results):
            if result is not None:
                all_results.append(result)
                logger.info(f"✅ Got info for player {player_id}")
            else:
                logger.warning(f"⚠️ Skipped player {player_id}")


        if i + batch_size < total:
            logger.info("Waiting 2 seconds before next batch...")
            await asyncio.sleep(2)

    return all_results


def run_player_info_ingestion():
    today_date = date.today()
    file_path = f"{BRONZE_DIR}/players_info/ingest_date={today_date}/players_info.json"

    if os.path.exists(file_path):
        logger.warning(f"Already ingested for {today_date}, skipping")
        return

    players_path_file = f"{BRONZE_DIR}/players/ingest_date={today_date}/players.json"

    if not os.path.exists(players_path_file):
        logger.error(f"Players file not found: {players_path_file}")
        return

    all_players = pd.read_json(players_path_file)
    players_ids = all_players["id"].tolist()
    logger.info(f"Found {len(players_ids)} players to fetch")


    all_results = asyncio.run(run_ingestion_async(players_ids))

    os.makedirs(f"{BRONZE_DIR}/players_info/ingest_date={today_date}/", exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(all_results, f, indent=4)

    logger.info(f"✅ Saved {len(all_results)} players to {file_path}")


if __name__ == "__main__":
    run_player_info_ingestion()