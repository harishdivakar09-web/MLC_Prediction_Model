import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('bmh')
plt.figure(figsize= (14,10))

#Creating dataframes for each csv file
batting_raw = pd.read_csv('batters.csv')
all_rounder_raw = pd.read_csv('all_rounders.csv')
bowling_raw = pd.read_csv('bowlers.csv')
team_raw = pd.read_csv('team_season.csv')



#-------TEAM SCORE CODE---------
team_mod = team_raw.copy()
#Modification of team.season.csv to include win percentage and dropping wins and losses columns
team_mod['win_percentage_2023'] = round((team_raw['wins_2023']/(team_raw['wins_2023']+team_raw['losses_2023']))*100,4)
team_mod['win_percentage_2024'] = round((team_raw['wins_2024']/(team_raw['wins_2024']+team_raw['losses_2024']))*100,4)
team_mod['win_percentage_2025'] = round((team_raw['wins_2025']/(team_raw['wins_2025']+team_raw['losses_2025']))*100,4)
team_mod.drop(columns = ['wins_2023', 'losses_2023','wins_2024','losses_2024','wins_2025','losses_2025'], inplace = True)

#Creating line graphs to analyze trends between years and quantitative variables
years = [2023, 2024, 2025]
y_axis_graphs = [['nrr_2023', 'nrr_2024', 'nrr_2025'], ['win_percentage_2023', 'win_percentage_2024', 'win_percentage_2025']]
y_axis_labels = ['NRR' , 'Win Percentage']

for _ in range(2):
    for index in range(6):
        plt.plot(years, team_mod.iloc[index][y_axis_graphs[_]])
    plt.xlabel('Year', labelpad= 5)
    plt.xticks(years)
    plt.ylabel(y_axis_labels[_], labelpad = 5)
    plt.grid(True, alpha=0.5)
    plt.legend(team_mod['team_abrv'], loc = 'center left' , bbox_to_anchor = (1,0.5))
    plt.show()



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
    '3rd' : 0.4,
    'Runner Up' : 0.8,
    'Winner' : 1.0
}

team_mod['standings_2023'] = team_mod['standings_2023'].str.strip().map(standing_points)
team_mod['standings_2024'] = team_mod['standings_2024'].str.strip().map(standing_points)
team_mod['standings_2025'] = team_mod['standings_2025'].str.strip().map(standing_points)



#Weight assignment (Team weightings to be adjusted)
weight_1 = 0.35
weight_2 = 0.2
weight_3 = 0.19246



weights_team= pd.Series({
    'nrr_2023': weight_3**3,
    'win_percentage_2023': weight_1**3,
    'standings_2023': weight_2**3,
    'nrr_2024': weight_3**2,
    'win_percentage_2024': weight_1**2,
    'standings_2024': weight_2**2,
    'nrr_2025': weight_3,
    'win_percentage_2025': weight_1,
    'standings_2025': weight_2
})

#Final team score
team_score = pd.DataFrame({
    'team_abrv' : team_raw['team_abrv'],
    'team_score' : round(team_mod[weights_team.index].dot(weights_team), 4)
}).sort_values(by = 'team_abrv').reset_index(drop=True)
team_score.iloc[5,0] = 'WAF'



#-------BATTING SCORE---------

batting_mod_1 = batting_raw.copy()

#Graphing batting categories to visualize skewness
plt.boxplot(batting_mod_1.loc[:, 'MLC_strike_rate' : ], orientation = 'horizontal')
plt.yticks(ticks = [1,2,3,4], labels = ['Strike Rate', 'Average', 'Fours', 'Sixes'])
plt.ylabel('Batting Category')
plt.show()

#Normalization of Strike Rate, Average, Fours, and Sixes
batting_mod_1['MLC_strike_rate'] = round((batting_mod_1['MLC_strike_rate']-batting_mod_1['MLC_strike_rate'].min())/(batting_mod_1['MLC_strike_rate'].max()-batting_mod_1['MLC_strike_rate'].min()),4)
batting_mod_1['MLC_average'] = round((batting_mod_1['MLC_average']-batting_mod_1['MLC_average'].min())/(batting_mod_1['MLC_average'].max()-batting_mod_1['MLC_average'].min()),4)
batting_mod_1['MLC_fours'] = round((batting_mod_1['MLC_fours']-batting_mod_1['MLC_fours'].min())/(batting_mod_1['MLC_fours'].max()-batting_mod_1['MLC_fours'].min()),4)
batting_mod_1['MLC_sixes'] = round((batting_mod_1['MLC_sixes']-batting_mod_1['MLC_sixes'].min())/(batting_mod_1['MLC_sixes'].max()-batting_mod_1['MLC_sixes'].min()),4)

#Aggregating player statistics into team statistics
batting_list = list(batting_mod_1.columns)
batting_mod_2 = batting_mod_1.groupby('team_abrv_unordered')[batting_list[4:]].mean().round(4).reset_index()




#Weight assignment
weights_batting= pd.Series({
    'MLC_strike_rate': 0.3,
    'MLC_average': 0.4,
    'MLC_fours': 0.15,
    'MLC_sixes': 0.15
})

#Final batting score

batting_score = pd.DataFrame({
    'team_abrv' : batting_mod_2['team_abrv_unordered'],
    'batting_score' : round(batting_mod_2[weights_batting.index].dot(weights_batting), 4)
}).sort_values(by = 'team_abrv').reset_index(drop=True)


#-------BOWLING SCORE---------
#Normalization of Wickets, Economy, Strike Rate, and Average
bowling_mod_1 = bowling_raw.copy()
bowling_mod_1['MLC_wickets'] = round((bowling_mod_1['MLC_wickets']-bowling_mod_1['MLC_wickets'].min())/(bowling_mod_1['MLC_wickets'].max()-bowling_mod_1['MLC_wickets'].min()),4)
bowling_mod_1['MLC_economy'] = round((bowling_mod_1['MLC_economy']-bowling_mod_1['MLC_economy'].max())/(bowling_mod_1['MLC_economy'].min()-bowling_mod_1['MLC_economy'].max()),4)
bowling_mod_1['MLC_strike_rate'] = round((bowling_mod_1['MLC_strike_rate']-bowling_mod_1['MLC_strike_rate'].max())/(bowling_mod_1['MLC_strike_rate'].min()-bowling_mod_1['MLC_strike_rate'].max()),4)
bowling_mod_1['MLC_average'] = round((bowling_mod_1['MLC_average']-bowling_mod_1['MLC_average'].max())/(bowling_mod_1['MLC_average'].min()-bowling_mod_1['MLC_average'].max()),4)



#Boxplot of bowling stats
plt.boxplot(bowling_mod_1.loc[:, 'MLC_wickets':], orientation = 'horizontal')
plt.yticks([1,2,3,4], list(bowling_mod_1.columns).replace("_"," ")[4:])
plt.show()
#Aggregating player statistics into team statistics
bowling_list = list(bowling_mod_1.columns)
bowling_mod_2 = bowling_mod_1.groupby('team_abrv')[bowling_list[4:]].mean().round(4).reset_index()





#Weight assignment
weights_bowling= pd.Series({
    'MLC_wickets': 0.1,
    'MLC_economy': 0.4,
    'MLC_strike_rate': 0.3,
    'MLC_average': 0.2
})

#Final bowling score
bowling_score = pd.DataFrame({
    'team_abrv' : bowling_mod_2['team_abrv'],
    'bowling_score' : round(bowling_mod_2[weights_bowling.index].dot(weights_bowling), 4)
}).sort_values(by = 'team_abrv').reset_index(drop=True)

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
all_rounder_list = list(all_rounder_mod_1.columns)
all_rounder_mod_2 = all_rounder_mod_1.groupby('team_abrv')[all_rounder_list[4:]].mean().round(4).reset_index()

#Weight assignment
weights_all_rounder= pd.Series({
    'MLC_strike_rate': 0.25,
    'MLC_average': 0.15,
    'MLC_fours': 0.005,
    'MLC_sixes': 0.005,
    'MLC_wickets': 0.005,
    'MLC_average_bowling': 0.005,
    'MLC_economy': 0.3,
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
    'team_score': 0.5,
    'batting_score': 0.1,
    'bowling_score': 0.1,
    'all_rounder_score': 0.3
})

#Final score
final_score = pd.DataFrame({
    'team_abrv' : all_scores['team_abrv'],
    'final_score' : round(all_scores[score_weights.index].dot(score_weights), 4)
}).sort_values(by = 'final_score', ascending=False).reset_index(drop=True)
print(final_score)