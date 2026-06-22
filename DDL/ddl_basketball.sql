create table league(
    league_id bigint identity (1,1) primary key,
    league_name nvarchar(200),
    league_location nvarchar(200)
);

insert into league(league_name, league_location)
values ('NBA', 'USA');

select *
from league;

create table season(
    season_id bigint identity (1,1) primary key,
    season nvarchar(100),
    league_id bigint,
    foreign key (league_id) references league(league_id)
);

insert into season(season, league_id)
values
    ('1985-86', 1),
    ('1986-87', 1),
    ('1987-88', 1),
    ('1988-89', 1),
    ('1989-90', 1),
    ('1990-91', 1),
    ('1991-92', 1),
    ('1992-93', 1),
    ('1993-94', 1),
    ('1994-95', 1),
    ('1995-96', 1),
    ('1996-97', 1),
    ('1997-98', 1),
    ('1998-99', 1),
    ('1999-00', 1),
    ('2000-01', 1),
    ('2001-02', 1),
    ('2002-03', 1),
    ('2003-04', 1),
    ('2004-05', 1),
    ('2005-06', 1),
    ('2006-07', 1),
    ('2007-08', 1),
    ('2008-09', 1),
    ('2009-10', 1),
    ('2010-11', 1),
    ('2011-12', 1),
    ('2012-13', 1),
    ('2013-14', 1),
    ('2014-15', 1),
    ('2015-16', 1),
    ('2016-17', 1),
    ('2017-18', 1),
    ('2018-19', 1),
    ('2019-20', 1),
    ('2020-21', 1),
    ('2021-22', 1),
    ('2022-23', 1),
    ('2023-24', 1),
    ('2024-25', 1),
    ('2025-26', 1);


create table player(
    player_id   bigint identity(1,1) primary key,
    source_player_id    bigint,
    full_name   nvarchar(200),
    birthdate   date,
    is_active   bit,
    height  nvarchar(100),
    weight  int,
    season_experience   int,
    position    nvarchar(100),
    from_year   nvarchar(50),
    to_year nvarchar(50),
    draft_year  nvarchar(50),
    draft_round nvarchar(50),
    draft_number    nvarchar(50),
    school  nvarchar(200),
    country nvarchar(200)
);


create table arena(
    arena_id bigint identity (1,1) primary key,
    arena_city nvarchar(100),
    arena_country nvarchar(100),
    arena_source_id bigint,
    arena_name nvarchar(100),
    arena_state nvarchar(100),
    arena_timezone nvarchar(100),
    team_source_id bigint
);

select *
from arena as a
where a.team_source_id = 1610612747;


create table team(
    team_id bigint identity (1,1) primary key,
    team_source_id bigint,
    team_city nvarchar(100),
    team_name nvarchar(100),
    full_team_name nvarchar(100),
    team_abbreviation nvarchar(100),
    conference nvarchar(100),
    division nvarchar(100),
    nickname nvarchar(100),
    year_founded int,
    owner nvarchar(100),
    general_manager nvarchar(100),
    head_coach nvarchar(100),
    d_league_affiliation nvarchar(100),
    logo_url NVARCHAR(500)
);

create table team_arena(
    arena_id bigint,
    team_id bigint,
    full_team_name nvarchar(100),
    arena_name nvarchar(100),
    is_current bit default 0,
    foreign key (arena_id) references arena(arena_id),
    foreign key (team_id) references team(team_id),
    primary key (arena_id,team_id)
);


select *
from team_arena as ta
where ta.is_current = 1
order by team_id;