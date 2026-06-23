from nba_api.stats.static import teams
import json, os
from datetime import date
from constants import BRONZE_DIR
from utils import get_logger

logger = get_logger("getting_all_teams.py")

def run_team_ingestion():

    today_date = date.today()
    file_path = f"{BRONZE_DIR}/teams/ingest_date={today_date}/teams.json"

    if os.path.exists(file_path):
        logger.warning(f"Data for the teams already ingested for {today_date}, skipping")
    else:
        logger.info("Fetching regular info for all the teams")
        try:

            all_teams = teams.get_teams()

            logger.info(f"Got the data, total {len(all_teams)} teams")

            os.makedirs(f"{BRONZE_DIR}/teams/ingest_date={today_date}/", exist_ok=True)

            with open(f"{BRONZE_DIR}/teams/ingest_date={today_date}/teams.json", "w") as f:
                json.dump(all_teams, f, indent=4)

            logger.info("Completed the ingestion process for the teams")

        except Exception as e:
            logger.error(f"Error: {repr(e)}")
            logger.error("Not completed the ingestion process for the teams")




if __name__ == "__main__":
    run_team_ingestion()