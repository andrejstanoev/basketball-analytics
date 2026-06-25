import time, os, pandas as pd
from nba_api.stats.endpoints import teaminfocommon, teamdetails
from utils import get_logger
from datetime import date
from constants import BRONZE_DIR

logger = get_logger("getting_team_details.py")

def run_team_details_ingestion():
    today_date = date.today()

    file_path = f"{BRONZE_DIR}/teams_details/ingest_date={today_date}/team_details.json"

    if os.path.exists(file_path):
        logger.warning(f"Data for team details already ingested for {today_date}, skipping")
    else:
        teams_path = f"{BRONZE_DIR}/teams/ingest_date={today_date}/teams.json"
        all_teams = pd.read_json(teams_path)

        team_ids = all_teams["id"].tolist()
        results = []
        for team_id in team_ids:
            try:
                logger.info(f"Fetching details for team with id={team_id}")
                dfs_1 = teaminfocommon.TeamInfoCommon(team_id=team_id).get_data_frames()
                team_common_df = dfs_1[0]

                dfs_2 = teamdetails.TeamDetails(team_id=team_id).get_data_frames()
                team_details_df = dfs_2[0]

                res = team_common_df.merge(right=team_details_df, how="inner", on="TEAM_ID")

                results.append(res)
                logger.info(f"Got details for team with id={team_id}")

            except Exception as e:
                logger.error(f"Error: {repr(e)}")

            time.sleep(3)

        final_df = pd.concat(results, ignore_index=True)

        os.makedirs(f"{BRONZE_DIR}/teams_details/ingest_date={today_date}/", exist_ok=True)

        final_df.to_json(f"{BRONZE_DIR}/teams_details/ingest_date={today_date}/team_details.json", orient="records", indent=4)

if __name__ == "__main__":
    run_team_details_ingestion()