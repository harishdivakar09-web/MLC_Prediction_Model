import pandas as pd

#Creating dataframes for each csv file
batting_raw = pd.read_csv('batters.csv')
all_rounder_raw = pd.read_csv('all_rounders.csv')
bowling_raw = pd.read_csv('bowlers.csv')
team_raw = pd.read_csv('team_season.csv')

#-------TEAM SCORE CODE---------
#Modification of team.season.csv to include win percentage and dropping wins and losses columns
team_raw['win_percentage_2023'] = round((team_raw['wins_2023']/(team_raw['wins_2023']+team_raw['losses_2023']))*100,4)
team_raw['win_percentage_2024'] = round((team_raw['wins_2024']/(team_raw['wins_2024']+team_raw['losses_2024']))*100,4)
team_raw['win_percentage_2025'] = round((team_raw['wins_2025']/(team_raw['wins_2025']+team_raw['losses_2025']))*100,4)
team_mod = team_raw.drop(columns = ['wins_2023', 'losses_2023','wins_2024','losses_2024','wins_2025','losses_2025'])


#Normalization of NRR, Win Percentage, and Standings
team_mod['nrr_2023'] = round((team_mod['nrr_2023']-team_mod['nrr_2023'].min())/(team_mod['nrr_2023'].max()-team_mod['nrr_2023'].min()),4)
team_mod['nrr_2024'] = round((team_mod['nrr_2024']-team_mod['nrr_2024'].min())/(team_mod['nrr_2024'].max()-team_mod['nrr_2024'].min()),4)
team_mod['nrr_2025'] = round((team_mod['nrr_2025']-team_mod['nrr_2025'].min())/(team_mod['nrr_2025'].max()-team_mod['nrr_2025'].min()),4)
team_mod['win_percentage_2023'] = round((team_mod['win_percentage_2023']-team_mod['win_percentage_2023'].min())/(team_mod['win_percentage_2023'].max()-team_mod['win_percentage_2023'].min()),4)
team_mod['win_percentage_2024'] = round((team_mod['win_percentage_2024']-team_mod['win_percentage_2024'].min())/(team_mod['win_percentage_2024'].max()-team_mod['win_percentage_2024'].min()),4)
team_mod['win_percentage_2025'] = round((team_mod['win_percentage_2025']-team_mod['win_percentage_2025'].min())/(team_mod['win_percentage_2025'].max()-team_mod['win_percentage_2025'].min()),4)

standing_points= {
    'Group' : 0.0,
    '4th' : 0.25,
    '3rd' : 0.5,
    'Runner Up' : 0.75,
    'Winner' : 1.0
}

team_mod['standings_2023'] = team_mod['standings_2023'].str.strip().map(standing_points)
team_mod['standings_2024'] = team_mod['standings_2024'].str.strip().map(standing_points)
team_mod['standings_2025'] = team_mod['standings_2025'].str.strip().map(standing_points)

#Weight assignment (either standings biased, NRR biased, or Win Percentage biased) 

weights= pd.Series({
    'nrr_2023': 0.114**3,
    'win_percentage_2023': 0.2**3,
    'standings_2023': 0.4**3,
    'nrr_2024': 0.114*0.114,
    'win_percentage_2024': 0.2*0.2,
    'standings_2024': 0.4*0.4,
    'nrr_2025': 0.114,
    'win_percentage_2025': 0.2,
    'standings_2025': 0.4
})
team_score = pd.DataFrame({
    'team_abrv' : team_raw['team_abrv'],
    'team_score' : round(team_mod[weights.index].dot(weights), 4)
})

print(team_score.head())

#-------BATTING SCORE CODE---------