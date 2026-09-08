from constants import DUCK_DB_FILE_PATH
import duckdb
from utils import get_logger

logger = get_logger("dim_game_etl.py")

logger.info("Creating a connection")
connection = duckdb.connect(DUCK_DB_FILE_PATH)
logger.info("Created a connection to the database")

logger.info("Starting process...")
connection.sql("""
insert into dim_game(game_id, home_team_id, home_team_name, away_team_id, away_team_name, winner_team_id, winner_team_name, loser_team_id, loser_team_name, season, game_date, game_type)
select g.GAME_ID as game_id,
       g.home_team_id,
       ht.full_team_name as home_team_name,
       g.away_team_id,
       a_t.full_team_name as away_team_name,
       g.winner_team_id,
       wt.full_team_name as winner_team_name,
       g.loser_team_id,
       lt.full_team_name as loser_team_name,
       g.season,
       g.game_date,
       g.type
from read_parquet('silver/games/*.parquet') as g
join read_parquet('silver/teams/*.parquet') as ht on g.home_team_id = ht.team_source_id
join read_parquet('silver/teams/*.parquet') as a_t on g.away_team_id = a_t.team_source_id
join read_parquet('silver/teams/*.parquet') as wt on g.winner_team_id = wt.team_source_id
join read_parquet('silver/teams/*.parquet') as lt on g.loser_team_id = lt.team_source_id
left join dim_game as dg on dg.game_id = g.GAME_ID
where dg.game_id is null;
""")
logger.info("Finished process")

logger.info("Closing the connection")
connection.close()
logger.info("Closed the connection")