from nba_api.stats.endpoints import playergamelogs
import json, os, time
from constants import BRONZE_DIR, CURRENT_SEASON
from utils import get_all_seasons, get_logger

def run_games_players_ingestion():

    seasons = get_all_seasons()

    season_types = {
        'Regular Season': 'regular',
        'Playoffs': 'playoffs'
    }

    logger = get_logger("getting_all_games_players.py")

    for s in seasons:
        if s != CURRENT_SEASON and os.path.exists(f"{BRONZE_DIR}/players_games/season={s}"):
            logger.info(f"Skipping for season {s}")
            continue
        else:
            os.makedirs(f"{BRONZE_DIR}/players_games/season={s}",exist_ok=True)

            for season_type, label in season_types.items():
                try:
                    logger.info(f"Fetching {s} {season_type}...")

                    data = playergamelogs.PlayerGameLogs(season_nullable=s,season_type_nullable=season_type)

                    logger.info(f"Fetched data for {s} {season_type} ")

                    data_json = json.loads(data.get_normalized_json())

                    os.makedirs(f"{BRONZE_DIR}/players_games/season={s}/type={label}", exist_ok=True)

                    with open(f"{BRONZE_DIR}/players_games/season={s}/type={label}/games.json","w") as f:
                        json.dump(data_json,f,indent=4)

                    logger.info(f"Saved for season {s} - {label}")

                except Exception as e:
                    logger.error(f"Error: {repr(e)}")

                time.sleep(4)

if __name__ == "__main__":
    run_games_players_ingestion()