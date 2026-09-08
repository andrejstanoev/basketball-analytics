from constants import DUCK_DB_FILE_PATH
import duckdb
from utils import get_logger

logger = get_logger("fact_team_games_etl.py")

logger.info("Creating a connection")
connection = duckdb.connect(DUCK_DB_FILE_PATH)
logger.info("Created a connection to the database")

logger.info("Starting process...")
connection.sql("""
set variable last_job_date = (
    select coalesce(
        (select e.date
         from etl_log AS e
         where e.job_name = 'fact_team_games' and e.state = 'DONE'
         order by e.date desc
         limit 1),
        date '1600-01-01'
    )
);

select getvariable('last_job_date') as res;

insert into fact_team_games(season, type, team_skey, game_skey, game_date, win_loss, minutes, points, assists, defensive_rebounds, offensive_rebounds, rebounds, blocks, field_goals_3_attempted, field_goals_3_made, field_goals_3_percentage, field_goals_attempted, field_goals_made, field_goals_percentage, free_throws_attempted, free_throws_made, free_throw_percentage, personal_fouls, steals, turnovers, plus_minus)
select tg.season,
       tg.type,
       dt.SKey as team_skey,
       dg.SKey as game_skey,
       tg.game_date,
       tg.win_loss,
       tg.minutes,
       tg.points,
       tg.assists,
       tg.defensive_rebounds,
       tg.offensive_rebounds,
       tg.rebounds,
       tg.blocks,
       tg.field_goals_3_attempted,
       tg.field_goals_3_made,
       tg.field_goal_3_percentage,
       tg.field_goals_attempted,
       tg.field_goals_made,
       tg.field_goal_percentage,
       tg.free_throws_attempted,
       tg.free_throws_made,
       tg.free_throw_percentage,
       tg.personal_fouls,
       tg.steals,
       tg.turnovers,
       tg.plus_minus,
from read_parquet('silver/teams_games/*.parquet') as tg
join dim_team as dt on dt.team_id = tg.team_id
join dim_game as dg on dg.game_id = tg.game_id
where tg.last_modified > getvariable('last_job_date');

insert into etl_log(job_name, state, "date")
VALUES (
        'fact_team_games',
        'DONE',
        current_date
       );
""")
logger.info("Finished process")

logger.info("Closing the connection")
connection.close()
logger.info("Closed the connection")