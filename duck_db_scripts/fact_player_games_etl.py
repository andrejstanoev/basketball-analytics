from constants import DUCK_DB_FILE_PATH
import duckdb
from utils import get_logger

logger = get_logger("fact_player_games_etl.py")

logger.info("Creating a connection")
connection = duckdb.connect(DUCK_DB_FILE_PATH)
logger.info("Created a connection to the database")

logger.info("Starting process...")
connection.sql("""
set variable last_job_date = (
    select coalesce(
        (select e.date
         from etl_log AS e
         where e.job_name = 'fact_player_games' and e.state = 'DONE'
         order by e.date desc
         limit 1),
        date '1600-01-01'
    )
);

select getvariable('last_job_date') as res;

insert into fact_player_games(season, type, player_skey, game_skey, team_skey, game_date, minutes, points, assists, blocks, blocks_against, has_double_double, has_triple_double, defensive_rebounds, offensive_rebounds, rebounds, steals, turnovers, field_goals_3_attempted, field_goals_3_made, field_goals_3_percentage, field_goals_attempted, field_goals_made, field_goals_percentage, free_throws_attempted, free_throws_made, free_throw_percentage, personal_fouls, personal_fouls_drawn, plus_minus)
select pg.season,
       pg.type,
       dp.SKey AS player_skey,
       dg.SKey AS game_skey,
       dt.SKey AS team_skey,
       pg.game_date,
       pg.minutes,
       pg.points,
       pg.assists,
       pg.blocks,
       pg.blocks_against,
       pg.has_double_double,
       pg.has_triple_double,
       pg.defensive_rebounds,
       pg.offensive_rebounds,
       pg.rebounds,
       pg.steals,
       pg.turnovers,
       pg.field_goals_3_attempted,
       pg.field_goals_3_made,
       pg.field_goals_3_percentage,
       pg.field_goals_attempted,
       pg.field_goals_made,
       pg.field_goals_percentage,
       pg.free_throws_attempted,
       pg.free_throws_made,
       pg.free_throw_percentage,
       pg.personal_fouls,
       pg.personal_fouls_drawn,
       pg.plus_minus,
from read_parquet('silver/player_games/*/*.parquet', hive_partitioning = true) as pg
join dim_game as dg on dg.game_id = pg.game_id
join dim_player as dp on dp.player_id = pg.player_id
join dim_team as dt on dt.team_id = pg.team_id
where pg.last_modified > getvariable('last_job_date');


insert into etl_log(job_name, state, "date")
VALUES (
        'fact_player_games',
        'DONE',
        current_date
       );

""")
logger.info("Finished process")

logger.info("Closing the connection")
connection.close()
logger.info("Closed the connection")