from nba_api.stats.endpoints import leaguegamelog
import json, time, os
from utils import get_all_seasons, get_logger
from constants import BRONZE_DIR, CURRENT_SEASON

seasons = get_all_seasons()

season_types = {
    'Regular Season': 'regular',
    'Playoffs': 'playoffs'
}

logger = get_logger("getting_all_games")

for s in seasons:
    if s != CURRENT_SEASON and os.path.exists(f"{BRONZE_DIR}/games/season={s}"):
        logger.info(f"Skipping for season {s}")
        continue
    else:
        os.makedirs(f"{BRONZE_DIR}/games/season={s}", exist_ok=True)

        for season_type, label in season_types.items():
            try:
                logger.info(f"Fetching {s} {season_type}...")
                games = leaguegamelog.LeagueGameLog(
                    season=s,
                    season_type_all_star=season_type
                )
                data = json.loads(games.get_normalized_json())

                with open(f"{BRONZE_DIR}/games/season={s}/games_{s}_{label}_log.json","w") as f:
                    json.dump(data, f, indent=4)

                logger.info(f"Saved games for {s} {label}")

            except Exception as e:
                logger.error(f"Error: {repr(e)}")

            time.sleep(4)
