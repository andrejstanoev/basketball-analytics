from constants import DUCK_DB_FILE_PATH
import duckdb
from utils import get_logger

logger = get_logger("dim_player_etl.py")

logger.info("Creating a connection")
connection = duckdb.connect(DUCK_DB_FILE_PATH)
logger.info("Created a connection to the database")

logger.info("Starting process...")
connection.sql("""
create temp table temp_player as
with source as (
    select p.player_source_id as player_id,
       p.full_name,
       p.birthdate,
       p.is_active,
       p.height,
       p.weight,
       p.season_experience,
       p.position,
       p.draft_year,
       p.draft_number,
       p.school,
       p.country,
       sha256( cast(p.player_source_id as varchar) ) as SCD_KeyHash,
       sha256( concat_ws( ';', p.full_name, cast(p.is_active as varchar), p.height, cast(p.weight as varchar), cast(p.season_experience as varchar), p.position  ) ) as SCD_ColumnHash
    from read_parquet('silver/players/*.parquet') as p
)
select s.*,
       case
           when dp.SCD_KeyHash is null then 'new'
           when dp.SCD_ColumnHash != s.SCD_ColumnHash then 'modified'
           else 'same'
       end as record_type,
       case
           when dp.SKey is null then null
           when dp.SCD_FirstKey is null then dp.SKey
           else dp.SCD_FirstKey
       end as SCD_FirstKey
from source as s
left join dim_player as dp on s.SCD_KeyHash = dp.SCD_KeyHash;


update dim_player
set SCD_IsCurrent = false,
    SCD_ValidTo = now()
from temp_player as tp
where dim_player.SCD_IsCurrent = true and tp.record_type = 'modified' and tp.SCD_KeyHash = dim_player.SCD_KeyHash;

insert into dim_player(player_id, full_name, birthdate, is_active, height, weight, season_experience, "position", draft_year, draft_number, school, country, SCD_KeyHash, SCD_ColumnHash, SCD_ValidFrom, SCD_ValidTo, SCD_IsCurrent, SCD_FirstKey)
select tp.player_id,
       tp.full_name,
       tp.birthdate,
       tp.is_active,
       tp.height,
       tp.weight,
       tp.season_experience,
       tp.position,
       tp.draft_year,
       tp.draft_number,
       tp.school,
       tp.country,
       tp.SCD_KeyHash,
       tp.SCD_ColumnHash,
       now() as SCD_ValidFrom,
       '9999-12-31'::timestamp as SCD_ValidTo,
       1 as SCD_IsCurrent,
       tp.SCD_FirstKey
from temp_player as tp
where tp.record_type = 'modified' or tp.record_type = 'new';
""")
logger.info("Finished process")

logger.info("Closing the connection")
connection.close()
logger.info("Closed the connection")