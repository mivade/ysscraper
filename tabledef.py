"""Definition of the SQL table fomats.

Notes
-----

Yahoo reports scaking as the number of times a QB was sacked rather than
as a defensive stat.

Passing attempts and completions are listed as just one stat in the form
"x-y" for x completions out of y attempts in the "Comp-Att"
statistic. This is split into two columns in the table format.

"""

# SQL code for generating the game stats table.
game_stats = """CREATE TABLE `game_stats` (
    `id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `date` TEXT,
    `away_team` TEXT,
    `home_team` TEXT,
    `away_score` INTEGER,
    `home_score` INTEGER,
    `away_first_downs` INTEGER,
    `home_first_downs` INTEGER,
    `away_total_yards` INTEGER,
    `home_total_yards` INTEGER,
    `away_turnovers` INTEGER,
    `home_turnovers` INTEGER,
    `away_third_down_efficiency` TEXT,
    `home_third_down_efficiency` TEXT,
    `away_fourth_down_efficiency` TEXT,
    `home_fourth_down_efficiency` TEXT,
    `away_total_plays` INTEGER,
    `home_total_plays` INTEGER,
    `away_avg_gain_per_play` REAL,
    `home_avg_gain_per_play` REAL,
    `away_rush_yards` INTEGER,
    `home_rush_yards` INTEGER,
    `away_rush_plays` INTEGER,
    `home_rush_plays` INTEGER,
    `away_yards_per_rush` REAL,
    `home_yards_per_rush` REAL,
    `away_pass_yards` INTEGER,
    `home_pass_yards` INTEGER,
    `away_pass_completions` INTEGER,
    `home_pass_completions` INTEGER,
    `away_pass_attempts` INTEGER,
    `home_pass_attempts` INTEGER,
    `away_yards_per_pass` REAL,
    `home_yards_per_pass` REAL,
    `away_sacked` INTEGER,
    `home_sacked` INTEGER,
    `away_sack_yards` INTEGER,
    `home_sack_yards` INTEGER,
    `away_interceptions` INTEGER,
    `home_interceptions` INTEGER,
    `away_punts` INTEGER,
    `home_punts` INTEGER,
    `away_punt_avg` REAL,
    `home_punt_avg` REAL,
    `away_penalties` INTEGER,
    `home_penalties` INTEGER,
    `away_penalty_yards` INTEGER,
    `home_penalty_yards` INTEGER,
    `away_fumbles` INTEGER,
    `home_fumbles` INTEGER,
    `away_fumbles_lost` INTEGER,
    `home_fumbles_lost` INTEGER
);"""

# SQL code for generating the teams table.
teams = """CREATE TABLE `teams` (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`name`	TEXT NOT NULL,
	`division`	TEXT,
	`conference`	TEXT,
	`conference_division`	TEXT,
	`wins`	INTEGER,
	`losses`	INTEGER
);"""

