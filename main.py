import pandas as pd

#Creating dataframes for each csv file
batting_raw = pd.read_csv('batters.csv')
all_rounder_raw = pd.read_csv('all_rounders.csv')
bowling_raw = pd.read_csv('bowlers.csv')
team_raw = pd.read_csv('team_season.csv')

#Team score
print(team_raw.head())
team_score = 2



