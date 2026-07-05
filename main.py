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
weight_1 = 0.4
weight_2 = 0.2
weight_3 = 0.114

weights_team= pd.Series({
    'nrr_2023': weight_3**3,
    'win_percentage_2023': weight_2**3,
    'standings_2023': weight_1**3,
    'nrr_2024': weight_3**2,
    'win_percentage_2024': weight_2**2,
    'standings_2024': weight_1**2,
    'nrr_2025': weight_3,
    'win_percentage_2025': weight_2,
    'standings_2025': weight_1
})

#Final team score
team_score = pd.DataFrame({
    'team_abrv' : team_raw['team_abrv'],
    'team_score' : round(team_mod[weights_team.index].dot(weights_team), 4)
})
team_score = team_score.sort_values(by = 'team_abrv').reset_index(drop=True)
team_score.iloc[5,0] = 'WAF'

# print(team_score)

#-------BATTING SCORE---------

batting_mod_1 = batting_raw.copy()

#Normalization of Strike Rate, Average, Fours, and Sixes
batting_mod_1['MLC_strike_rate'] = round((batting_mod_1['MLC_strike_rate']-batting_mod_1['MLC_strike_rate'].min())/(batting_mod_1['MLC_strike_rate'].max()-batting_mod_1['MLC_strike_rate'].min()),4)
batting_mod_1['MLC_average'] = round((batting_mod_1['MLC_average']-batting_mod_1['MLC_average'].min())/(batting_mod_1['MLC_average'].max()-batting_mod_1['MLC_average'].min()),4)
batting_mod_1['MLC_fours'] = round((batting_mod_1['MLC_fours']-batting_mod_1['MLC_fours'].min())/(batting_mod_1['MLC_fours'].max()-batting_mod_1['MLC_fours'].min()),4)
batting_mod_1['MLC_sixes'] = round((batting_mod_1['MLC_sixes']-batting_mod_1['MLC_sixes'].min())/(batting_mod_1['MLC_sixes'].max()-batting_mod_1['MLC_sixes'].min()),4)

#Aggregating player statistics into team statistics
batting_mod_2 = batting_mod_1.groupby('team_abrv_unordered').agg({
    'MLC_strike_rate': 'mean',
    'MLC_average': 'mean',
    'MLC_fours': 'mean',
    'MLC_sixes': 'mean'
}).reset_index()
batting_mod_2[['MLC_strike_rate','MLC_average','MLC_fours','MLC_sixes']] = batting_mod_2[[ 'MLC_strike_rate','MLC_average','MLC_fours','MLC_sixes']].round(4)

#Weight assignment
weights_batting= pd.Series({
    'MLC_strike_rate': 0.35,
    'MLC_average': 0.4,
    'MLC_fours': 0.125,
    'MLC_sixes': 0.125
})

#Final batting score

batting_score = pd.DataFrame({
    'team_abrv' : batting_mod_2['team_abrv_unordered'],
    'batting_score' : round(batting_mod_2[weights_batting.index].dot(weights_batting), 4)
})
batting_score = batting_score.sort_values(by = 'team_abrv').reset_index(drop=True)
# print(batting_score)

#-------BOWLING SCORE---------
#Normalization of Wickets, Economy, Strike Rate, and Average
bowling_mod_1 = bowling_raw.copy()
bowling_mod_1['MLC_wickets'] = round((bowling_mod_1['MLC_wickets']-bowling_mod_1['MLC_wickets'].min())/(bowling_mod_1['MLC_wickets'].max()-bowling_mod_1['MLC_wickets'].min()),4)
bowling_mod_1['MLC_economy'] = round((bowling_mod_1['MLC_economy']-bowling_mod_1['MLC_economy'].max())/(bowling_mod_1['MLC_economy'].min()-bowling_mod_1['MLC_economy'].max()),4)
bowling_mod_1['MLC_strike_rate'] = round((bowling_mod_1['MLC_strike_rate']-bowling_mod_1['MLC_strike_rate'].min())/(bowling_mod_1['MLC_strike_rate'].max()-bowling_mod_1['MLC_strike_rate'].min()),4)
bowling_mod_1['MLC_average'] = round((bowling_mod_1['MLC_average']-bowling_mod_1['MLC_average'].min())/(bowling_mod_1['MLC_average'].max()-bowling_mod_1['MLC_average'].min()),4)

#Aggregating player statistics into team statistics
bowling_mod_2 = bowling_mod_1.groupby('team_abrv').agg({
    'MLC_wickets': 'mean',
    'MLC_economy': 'mean',
    'MLC_strike_rate': 'mean',
    'MLC_average': 'mean'
}).reset_index()
bowling_mod_2[['MLC_wickets','MLC_economy','MLC_strike_rate','MLC_average']] = bowling_mod_2[['MLC_wickets','MLC_economy','MLC_strike_rate','MLC_average']].round(4)

#Weight assignment
weights_bowling= pd.Series({
    'MLC_wickets': 0.1,
    'MLC_economy': 0.5,
    'MLC_strike_rate': 0.3,
    'MLC_average': 0.1
})

#Final bowling score
bowling_score = pd.DataFrame({
    'team_abrv' : bowling_mod_2['team_abrv'],
    'bowling_score' : round(bowling_mod_2[weights_bowling.index].dot(weights_bowling), 4)
})
bowling_score = bowling_score.sort_values(by = 'team_abrv').reset_index(drop=True)

#-------ALL-ROUNDER SCORE---------
all_rounder_mod_1 = all_rounder_raw.copy()
all_rounder_mod_1.rename(columns = {
    'MLC_average.1':'MLC_average_bowling',
    'MLC_strike_rate.1':'MLC_strike_rate_bowling'
}, inplace = True)

#Normalization of Strike Rate, Average, Fours, Sixes, Wickets, Economy, Strike Rate (Bowling), and Average (Bowling)
all_rounder_mod_1['MLC_strike_rate'] = round((all_rounder_mod_1['MLC_strike_rate']-all_rounder_mod_1['MLC_strike_rate'].min())/(all_rounder_mod_1['MLC_strike_rate'].max()-all_rounder_mod_1['MLC_strike_rate'].min()),4)
all_rounder_mod_1['MLC_average'] = round((all_rounder_mod_1['MLC_average']-all_rounder_mod_1['MLC_average'].min())/(all_rounder_mod_1['MLC_average'].max()-all_rounder_mod_1['MLC_average'].min()),4)
all_rounder_mod_1['MLC_fours'] = round((all_rounder_mod_1['MLC_fours']-all_rounder_mod_1['MLC_fours'].min())/(all_rounder_mod_1['MLC_fours'].max()-all_rounder_mod_1['MLC_fours'].min()),4)
all_rounder_mod_1['MLC_sixes'] = round((all_rounder_mod_1['MLC_sixes']-all_rounder_mod_1['MLC_sixes'].min())/(all_rounder_mod_1['MLC_sixes'].max()-all_rounder_mod_1['MLC_sixes'].min()),4)
all_rounder_mod_1['MLC_wickets'] = round((all_rounder_mod_1['MLC_wickets']-all_rounder_mod_1['MLC_wickets'].min())/(all_rounder_mod_1['MLC_wickets'].max()-all_rounder_mod_1['MLC_wickets'].min()),4)
all_rounder_mod_1['MLC_average_bowling'] = round((all_rounder_mod_1['MLC_average_bowling']-all_rounder_mod_1['MLC_average_bowling'].max())/(all_rounder_mod_1['MLC_average_bowling'].min()-all_rounder_mod_1['MLC_average_bowling'].max()),4)
all_rounder_mod_1['MLC_economy'] = round((all_rounder_mod_1['MLC_economy']-all_rounder_mod_1['MLC_economy'].max())/(all_rounder_mod_1['MLC_economy'].min()-all_rounder_mod_1['MLC_economy'].max()),4)
all_rounder_mod_1['MLC_strike_rate_bowling'] = round((all_rounder_mod_1['MLC_strike_rate_bowling']-all_rounder_mod_1['MLC_strike_rate_bowling'].max())/(all_rounder_mod_1['MLC_strike_rate_bowling'].min()-all_rounder_mod_1['MLC_strike_rate_bowling'].max()),4)

#Aggregating player statistics into team statistics
all_rounder_mod_2 = all_rounder_mod_1.groupby('team_abrv').agg({
    'MLC_strike_rate': 'mean',
    'MLC_average': 'mean',
    'MLC_fours': 'mean',
    'MLC_sixes': 'mean',
    'MLC_wickets': 'mean',
    'MLC_average_bowling': 'mean',
    'MLC_economy': 'mean',
    'MLC_strike_rate_bowling': 'mean'
}).round(4).reset_index()

#Weight assignment
weights_all_rounder= pd.Series({
    'MLC_strike_rate': 0.1,
    'MLC_average': 0.1,
    'MLC_fours': 0.05,
    'MLC_sixes': 0.05,
    'MLC_wickets': 0.2,
    'MLC_average_bowling': 0.2,
    'MLC_economy': 0.2,
    'MLC_strike_rate_bowling': 0.1
})

#Final all-rounder score
all_rounder_score = pd.DataFrame({
    'team_abrv' : all_rounder_mod_2['team_abrv'],
    'all_rounder_score' : round(all_rounder_mod_2[weights_all_rounder.index].dot(weights_all_rounder),4)
}).sort_values(by = 'team_abrv').reset_index(drop=True)

#Combining all scores into a single dataframe
all_scores = team_score.merge(batting_score, on = 'team_abrv', how ='left').merge(bowling_score, on = 'team_abrv', how = 'left').merge(all_rounder_score, on = 'team_abrv', how = 'left')

score_weights = pd.Series({
    'team_score': 0.4,
    'batting_score': 0.2,
    'bowling_score': 0.2,
    'all_rounder_score': 0.2
})

#Final score
final_score = pd.DataFrame({
    'team_name' : all_scores['team_abrv'],
    'final_score' : round(all_scores[score_weights.index].dot(score_weights), 4)
})

print(final_score)