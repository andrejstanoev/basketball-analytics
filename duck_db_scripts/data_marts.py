from constants import DUCK_DB_FILE_PATH
import duckdb
from utils import get_logger


def create_data_marts():
    logger = get_logger("creating_data_marts.py")

    logger.info("Creating a connection")
    connection = duckdb.connect(DUCK_DB_FILE_PATH)
    logger.info("Created a connection to the database")

    connection.sql("""
        create or replace table mart_player_season as
        select fpg.player_id,
           fpg.season,
           fpg.type,
           round(avg(fpg.minutes),2) as average_minutes,
           round(avg(fpg.points),2) as average_points,
           round(avg(fpg.assists),2) as average_assists,
           round(avg(fpg.rebounds),2) as average_rebounds,
           round(avg(fpg.steals),2) as average_steals,
           round(avg(fpg.blocks),2) as average_blocks,
           round(avg(fpg.turnovers),2) as average_turnovers,
           round(sum(fpg.field_goals_made) / nullif(sum(fpg.field_goals_attempted), 0), 3) as field_goal_percentage,
           round(sum(fpg.field_goals_3_made) / nullif(sum(fpg.field_goals_3_attempted), 0), 3) as field_goal_3_percentage,
           round(sum(fpg.free_throws_made) / nullif(sum(fpg.free_throws_attempted), 0), 3) as free_throw_percentage,
           round(avg(fpg.personal_fouls),2) as average_personal_fouls,
           round(avg(fpg.personal_fouls_drawn),2) as average_personal_fouls_drawn,
           round(avg(fpg.plus_minus),2) as average_plus_minus,
        from fact_player_games as fpg
        group by fpg.player_id, fpg.season, fpg.type;
        
        create or replace table mart_player_career as
        select fpg.player_id,
           fpg.type,
           round(avg(fpg.minutes),2) as average_minutes,
           round(avg(fpg.points),2) as average_points,
           round(avg(fpg.assists),2) as average_assists,
           round(avg(fpg.rebounds),2) as average_rebounds,
           round(avg(fpg.steals),2) as average_steals,
           round(avg(fpg.blocks),2) as average_blocks,
           round(avg(fpg.turnovers),2) as average_turnovers,
           round(sum(fpg.field_goals_made) / nullif(sum(fpg.field_goals_attempted), 0), 3) as field_goal_percentage,
           round(sum(fpg.field_goals_3_made) / nullif(sum(fpg.field_goals_3_attempted), 0), 3) as field_goal_3_percentage,
           round(sum(fpg.free_throws_made) / nullif(sum(fpg.free_throws_attempted), 0), 3) as free_throw_percentage,
           round(avg(fpg.personal_fouls),2) as average_personal_fouls,
           round(avg(fpg.personal_fouls_drawn),2) as average_personal_fouls_drawn,
           round(avg(fpg.plus_minus),2) as average_plus_minus,
        from fact_player_games as fpg
        group by fpg.player_id, fpg.type;
        
        create or replace table mart_player_team as
        select fpg.player_id,
           fpg.team_id,
           fpg.type,
           round(avg(fpg.minutes),2) as average_minutes,
           round(avg(fpg.points),2) as average_points,
           round(avg(fpg.assists),2) as average_assists,
           round(avg(fpg.rebounds),2) as average_rebounds,
           round(avg(fpg.steals),2) as average_steals,
           round(avg(fpg.blocks),2) as average_blocks,
           round(avg(fpg.turnovers),2) as average_turnovers,
           round(sum(fpg.field_goals_made) / nullif(sum(fpg.field_goals_attempted), 0), 3) as field_goal_percentage,
           round(sum(fpg.field_goals_3_made) / nullif(sum(fpg.field_goals_3_attempted), 0), 3) as field_goal_3_percentage,
           round(sum(fpg.free_throws_made) / nullif(sum(fpg.free_throws_attempted), 0), 3) as free_throw_percentage,
           round(avg(fpg.personal_fouls),2) as average_personal_fouls,
           round(avg(fpg.personal_fouls_drawn),2) as average_personal_fouls_drawn,
           round(avg(fpg.plus_minus),2) as average_plus_minus,
        from fact_player_games as fpg
        group by fpg.player_id, fpg.team_id, fpg.type;
        
        create or replace table mart_player_season_advanced as
        select player_id,
           season,
           type,
           count(*) as games,
           round(sum(points) / nullif(2.0 * (sum(field_goals_attempted) + 0.44 * sum(free_throws_attempted)), 0), 3) as true_shooting_pct,
           round((sum(field_goals_made) + 0.5 * sum(field_goals_3_made)) / nullif(sum(field_goals_attempted), 0), 3) as effective_fg_pct,
           round(sum(points) * 36.0 / nullif(sum(minutes), 0), 1) as points_per_36,
           round(sum(assists) / nullif(sum(turnovers), 0), 2)     as assist_to_turnover
        from fact_player_games
        group by all;
        
        create or replace table mart_player_rankings as
        select
        player_id,
        season,
        type,
        average_points,
        average_assists,
        average_rebounds,
        rank() over (
            partition by season, type
            order by average_points desc
        ) as points_rank,
        rank() over (
            partition by season, type
            order by average_assists desc
        ) as assists_rank,
        rank() over (
            partition by season, type
            order by average_rebounds desc
        ) as rebounds_rank
        from mart_player_season;
        
        select *
        from mart_player_rankings;
        
        create or replace table mart_player_rolling as
        select
        player_id,
        team_id,
        season,
        type,
        game_date,
        points,
        assists,
        rebounds,
        round(
            avg(points) over (
                partition by player_id, season, type
                order by game_date
                rows between 4 preceding and current row
            ), 2
        ) as points_last_5,
        round(
            avg(assists) over (
                partition by player_id, season, type
                order by game_date
                rows between 4 preceding and current row
            ), 2
        ) as assists_last_5,
        round(
            avg(rebounds) over (
                partition by player_id, season, type
                order by game_date
                rows between 4 preceding and current row
            ), 2
        ) as rebounds_last_5
        from fact_player_games;
        
    
        
        create or replace table mart_team_season as
        select ftg.team_id,
           ftg.season,
           ftg.type,
           sum(
            case
                when ftg.win_loss = 'W' then 1
                else 0
            end
           ) as total_wins,
           sum(
            case
                when ftg.win_loss = 'L' then 1
                else 0
            end
           ) as total_loses,
           round(avg(ftg.minutes),2) as average_minutes,
           round(avg(ftg.points),2) as average_points,
           round(avg(ftg.assists),2) as average_assists,
           round(avg(ftg.rebounds),2) as average_rebounds,
           round(avg(ftg.steals),2) as average_steals,
           round(avg(ftg.blocks),2) as average_blocks,
           round(avg(ftg.turnovers),2) as average_turnovers,
           round(sum(ftg.field_goals_made) / nullif(sum(ftg.field_goals_attempted), 0), 3) as field_goal_percentage,
           round(sum(ftg.field_goals_3_made) / nullif(sum(ftg.field_goals_3_attempted), 0), 3) as field_goal_3_percentage,
           round(sum(ftg.free_throws_made) / nullif(sum(ftg.free_throws_attempted), 0), 3) as free_throw_percentage,
           round(avg(ftg.personal_fouls),2) as average_personal_fouls,
           round(avg(ftg.plus_minus),2) as average_plus_minus
        from fact_team_games as ftg
        group by ftg.team_id, ftg.season, ftg.type;
        
        create or replace table mart_team_conference_standings as
        select dt.team_id,
           dt.full_team_name,
           mts.season,
           dt.conference,
           mts.total_wins,
           mts.total_loses,
           rank() over(
                partition by mts.season, mts.type, dt.conference
                order by mts.total_wins desc
           ) as position_standing
        from mart_team_season as mts
        join dim_team as dt on dt.team_id = mts.team_id
        where type = 'regular'
        order by season desc;
        
        create or replace table mart_team_career as
        select ftg.team_id,
           ftg.type,
           sum(
            case
                when ftg.win_loss = 'W' then 1
                else 0
            end
           ) as total_wins,
           sum(
            case
                when ftg.win_loss = 'L' then 1
                else 0
            end
           ) as total_loses,
           round(avg(ftg.minutes),2) as average_minutes,
           round(avg(ftg.points),2) as average_points,
           round(avg(ftg.assists),2) as average_assists,
           round(avg(ftg.rebounds),2) as average_rebounds,
           round(avg(ftg.steals),2) as average_steals,
           round(avg(ftg.blocks),2) as average_blocks,
           round(avg(ftg.turnovers),2) as average_turnovers,
           round(sum(ftg.field_goals_made) / nullif(sum(ftg.field_goals_attempted), 0), 3) as field_goal_percentage,
           round(sum(ftg.field_goals_3_made) / nullif(sum(ftg.field_goals_3_attempted), 0), 3) as field_goal_3_percentage,
           round(sum(ftg.free_throws_made) / nullif(sum(ftg.free_throws_attempted), 0), 3) as free_throw_percentage,
           round(avg(ftg.personal_fouls),2) as average_personal_fouls,
           round(avg(ftg.plus_minus),2) as average_plus_minus
        from fact_team_games as ftg
        group by ftg.team_id, ftg.type;

    """)

    logger.info("Closing the connection")
    connection.close()
    logger.info("Closed the connection")


if __name__ == "__main__":
    create_data_marts()