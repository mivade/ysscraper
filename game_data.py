"""Definition of the SQL table fomat.

Notes
-----

Yahoo reports scaking as the number of times a QB was sacked rather than
as a defensive stat.

Passing attempts and completions are listed as just one stat in the form
"x-y" for x completions out of y attempts in the "Comp-Att"
statistic. This is split into two columns in the table format.

"""

import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class GameData(Base):
    __tablename__ = 'game_stats'

    id = Column(Integer, primary_key=True, auto_increment=True)
    date = Column(Date)
    
    away_team = Column(String)
    home_team = Column(String)
    away_score = Column(Integer)
    home_score = Column(Integer)
    away_first_downs = Column(Integer)
    home_first_downs = Column(Integer)
    away_total_yards = Column(Integer)
    home_total_yards = Column(Integer)
    away_turnovers = Column(Integer)
    home_turnovers = Column(Integer)
    away_third_down_efficiency = Column(String)
    home_third_down_efficiency = Column(String)
    away_fourth_down_efficiency = Column(String)
    home_fourth_down_efficiency = Column(String)
    away_total_plays = Column(Integer)
    home_total_plays = Column(Integer)
    away_avg_gain_per_play = Column(Float)
    home_avg_gain_per_play = Column(Float)
    away_rush_yards = Column(Integer)
    home_rush_yards = Column(Integer)
    away_rush_plays = Column(Integer)
    home_rush_plays = Column(Integer)
    away_yards_per_rush = Column(Float)
    home_yards_per_rush = Column(Float)
    away_pass_yards = Column(Integer)
    home_pass_yards = Column(Integer)
    away_pass_completions = Column(Integer)
    home_pass_completions = Column(Integer)
    away_pass_attempts = Column(Integer)
    home_pass_attempts = Column(Integer)
    away_yards_per_pass = Column(Float)
    home_yards_per_pass = Column(Float)
    away_sacked = Column(Integer)
    home_sacked = Column(Integer)
    away_sack_yards = Column(Integer)
    home_sack_yards = Column(Integer)
    away_interceptions = Column(Integer)
    home_interceptions = Column(Integer)
    away_punts = Column(Integer)
    home_punts = Column(Integer)
    away_punt_avg = Column(Float)
    home_punt_avg = Column(Float)
    away_penalties = Column(Integer)
    home_penalties = Column(Integer)
    away_penalty_yards = Column(Integer)
    home_penalty_yards = Column(Integer)
    away_fumbles = Column(Integer)
    home_fumbles = Column(Integer)
    away_fumbles_lost = Column(Integer)
    home_fumbles_lost = Column(Integer)
    
    def __repr__(self):
        return "{:s} {:d}-{:d} {s}".format(
            self.away_team, self.away_score,
            self.home_score, self.home_team
        )
    
