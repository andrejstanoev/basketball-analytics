import pandas as pd
import time
from nba_api.stats.endpoints import teaminfocommon, teamdetails

all_teams = pd.read_json("../raw_data/all_teams.json")

all_teams_ids = all_teams["id"].tolist()

all_results = []
for team_id in all_teams_ids:
    try:
        df = teaminfocommon.TeamInfoCommon(team_id=team_id).get_data_frames()
        team_info_df = df[0]
        df_1 = teamdetails.TeamDetails(team_id=team_id).get_data_frames()
        team_details_df = df_1[0]
        res = team_info_df.merge(right=team_details_df,how="inner",on="TEAM_ID" )

        all_results.append(res)
        print(f"✅ Done team {team_id}")
    except Exception as e:
        print(f"❌ Failed team {team_id}: {e}")

    time.sleep(2)


final_df = pd.concat(all_results, ignore_index=True)

final_df.to_json("../raw_data/team_info/all_teams_info.json", orient="records", indent=4)