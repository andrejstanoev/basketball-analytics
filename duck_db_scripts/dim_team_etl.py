from constants import DUCK_DB_FILE_PATH
import duckdb
from utils import get_logger

logger = get_logger("dim_team_etl.py")

logger.info("Creating a connection")
connection = duckdb.connect(DUCK_DB_FILE_PATH)
logger.info("Created a connection to the database")

logger.info("Starting process...")
connection.sql("""
create temp table temp_team as
with source as (
    select t.team_source_id as team_id,
           t.team_city,
           t.team_name,
           t.full_team_name,
           t.team_abbreviation,
           t.conference,
           t.division,
           t.nickname,
           t.year_founded,
           t.owner,
           t.general_manager,
           t.head_coach,
           t.d_league_affiliation,
           t.state,
           sha256( cast(t.team_source_id as varchar) ) as SCD_KeyHash,
           sha256( concat_ws( ';', t.team_city, t.team_name, t.team_abbreviation, t.conference, t.division, t.nickname, t.owner, t.general_manager, t.head_coach, t.d_league_affiliation, t.state ) ) as SCD_ColumnHash
    from read_parquet('silver/teams/*.parquet') as t
)

select s.*,
       case
           when dt.SCD_KeyHash is null then 'new'
           when dt.SCD_ColumnHash != s.SCD_ColumnHash then 'modified'
           else 'same'
       end as record_type,
       case
           when dt.SKey is null then null
           when dt.SCD_FirstKey is null then dt.SKey
           else dt.SCD_FirstKey
       end as SCD_FirstKey
from source as s
left join dim_team as dt on dt.SCD_KeyHash = s.SCD_KeyHash;

select *
from temp_team;

update dim_team
set SCD_IsCurrent = false,
    SCD_ValidTo = now()
from temp_team as tm
where dim_team.SCD_IsCurrent = true and tm.record_type = 'modified' and tm.SCD_KeyHash = dim_team.SCD_KeyHash;

insert into dim_team(team_id, team_city, team_name, full_team_name, team_abbreviation, conference, division, nickname, year_founded, owner, general_manager, head_coach, d_league_affiliation, state, SCD_KeyHash, SCD_ColumnHash, SCD_ValidFrom, SCD_ValidTo, SCD_IsCurrent, SCD_FirstKey)
select tm.team_id,
       tm.team_city,
       tm.team_name,
       tm.full_team_name,
       tm.team_abbreviation,
       tm.conference,
       tm.division,
       tm.nickname,
       tm.year_founded,
       tm.owner,
       tm.general_manager,
       tm.head_coach,
       tm.d_league_affiliation,
       tm.state,
       tm.SCD_KeyHash,
       tm.SCD_ColumnHash,
       now() as SCD_ValidFrom,
       '9999-12-31'::timestamp as SCD_ValidTo,
       1 as SCD_IsCurrent,
       tm.SCD_FirstKey
from temp_team as tm
where tm.record_type = 'new' or tm.record_type = 'modified';
""")
logger.info("Finished process")

logger.info("Closing the connection")
connection.close()
logger.info("Closed the connection")