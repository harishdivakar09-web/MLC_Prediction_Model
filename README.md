# MLC Team Prediction Model

This project ranks Major League Cricket (MLC) teams using historical team results and player performance data. It combines recent team success, batting, bowling, and all-rounder statistics into one score. The team with the highest final score is treated as the strongest prediction based on the supplied data.

The model is a weighted scoring model rather than a trained machine-learning model. Its weights are chosen using cricket knowledge, recent-season importance, and visual analysis of the data with Matplotlib.

## Technologies Used

- **Python** runs the scoring and ranking process.
- **pandas** loads, cleans, normalizes, groups, weights, and combines the cricket data.
- **Matplotlib** displays trends and statistical distributions that help explain and justify the selected weights.
- **CSV files** store the team and player statistics used by the model.

## Project Files

- `main.py` contains the complete analysis and prediction process.
- `team_season.csv` contains team wins, losses, net run rate, and standings for 2023-2025.
- `batters.csv` contains player batting strike rate, average, fours, and sixes.
- `bowlers.csv` contains player wickets, bowling average, economy, and strike rate.
- `all_rounders.csv` contains batting and bowling statistics for all-rounders.

## Installation

Python 3 is required. Install the two project dependencies with:

```bash
pip install pandas matplotlib
```

Run the model from the project directory:

```bash
python main.py
```

Matplotlib opens several charts while the program runs. Close each chart window to allow the program to continue to the next chart and eventually print the final ranking in the terminal.

## How the Model Works

The program creates four category scores for every team:

1. Team score
2. Batting score
3. Bowling score
4. All-rounder score

Before applying weights, the numerical statistics are min-max normalized to values between `0` and `1`. This puts measurements with different units, such as win percentage, wickets, and economy rate, onto a comparable scale.

For statistics where a lower value is better, including bowling economy, bowling average, and bowling strike rate, the normalization is reversed. A lower raw value therefore produces a higher model score.

### Team Score

The team score uses results from the 2023, 2024, and 2025 seasons. pandas first calculates each season's win percentage:

```text
win percentage = wins / (wins + losses) * 100
```

The model then uses normalized net run rate, normalized win percentage, and a numerical value for the team's final standing:

| Standing | Score |
| --- | ---: |
| Group | 0.00 |
| 4th | 0.25 |
| 3rd | 0.40 |
| Runner Up | 0.80 |
| Winner | 1.00 |

The base team-performance weights are:

| Statistic | Base weight |
| --- | ---: |
| Net run rate | `0.19246` |
| Win percentage | `0.35` |
| Final standing | `0.20` |

Recency is built into the calculation. The 2025 values use the base weights, the 2024 weights are squared, and the 2023 weights are cubed. This reduces the influence of older seasons and gives the latest season the strongest effect on the prediction.

### Batting Score

The batting score uses four normalized player statistics:

| Statistic | Weight |
| --- | ---: |
| Strike rate | `0.50` |
| Batting average | `0.30` |
| Fours | `0.10` |
| Sixes | `0.10` |

pandas groups the batters by team and averages their normalized statistics. A dot product then applies the weights to produce one batting score per team. Strike rate and batting average receive the largest weights because they represent scoring speed and consistency, while boundary totals provide supporting evidence.

### Bowling Score

The bowling score uses:

| Statistic | Weight |
| --- | ---: |
| Wickets | `0.30` |
| Economy | `0.40` |
| Bowling strike rate | `0.20` |
| Bowling average | `0.10` |

Economy, strike rate, and average are reverse-normalized because lower values are better for a bowler. Economy receives the largest weight, followed by wickets, to reward teams that both limit runs and take wickets.

### All-Rounder Score

All-rounders are evaluated with both batting and bowling data:

| Statistic | Weight |
| --- | ---: |
| Batting strike rate | `0.30` |
| Batting average | `0.15` |
| Fours | `0.0045` |
| Sixes | `0.0045` |
| Wickets | `0.10` |
| Bowling average | `0.001` |
| Economy | `0.30` |
| Bowling strike rate | `0.05` |

The code renames the duplicate bowling average and strike-rate columns so they remain separate from the batting versions. It then normalizes the data, averages players by team, and applies the weights. Batting strike rate and bowling economy have the greatest influence because they capture an all-rounder's impact in both disciplines.

## How Matplotlib Helps Justify the Weights

Matplotlib does not calculate or train the weights. Instead, it provides visual checks that make the manual weighting decisions easier to explain:

- **Net run rate trend chart:** compares each team's NRR from 2023 through 2025 and shows how performance changes over time.
- **Win-percentage trend chart:** compares team success across the same seasons and supports placing more emphasis on recent form.
- **Batting box plot:** shows the spread and possible outliers in strike rate, average, fours, and sixes.
- **Bowling box plot:** shows the distributions of wickets, average, economy, and strike rate.
- **All-rounder box plot:** compares the spread of all eight batting and bowling measures used for all-rounders.

The trend charts support the model's recency weighting because they reveal whether a team's performance is improving or declining. The box plots reveal skewness, variation, and outliers, helping prevent a large raw scale or a few extreme players from silently determining the score. pandas normalization then converts those differently scaled statistics to a common range before the chosen weights are applied.

Together, Matplotlib provides the visual reasoning and pandas performs the numerical calculation.

## How pandas Builds the Prediction

pandas turns each CSV file into a DataFrame, similar to a spreadsheet table in Python. In `main.py`, it is used to:

- Load data with `pd.read_csv()`.
- Copy source data before modifying it.
- Calculate win percentages and other derived columns.
- Remove columns that are no longer needed.
- Clean and map text standings to numerical scores.
- Normalize statistics so different measurements can be compared fairly.
- Group players by team with `groupby()` and calculate team averages with `mean()`.
- Store weights in pandas Series objects.
- Calculate weighted scores efficiently with `dot()`.
- Merge the four category-score tables into one table.
- Sort teams from highest to lowest final score.

This workflow is what makes the prediction model practical: pandas converts raw player-level and season-level records into consistent team-level features, then combines those features into a reproducible ranking.

## Final Ranking

The four category scores are combined with these final weights:

| Category | Final weight |
| --- | ---: |
| Team score | `0.60` |
| Batting score | `0.05` |
| Bowling score | `0.15` |
| All-rounder score | `0.20` |

Historical team performance receives the largest share because it captures proven results across multiple seasons. Bowling and all-rounder strength receive the next-largest shares, while the separate batting score contributes the remaining amount.

The program prints a DataFrame containing `team_abrv` and `final_score`, sorted from the highest predicted score to the lowest.

## Model Limitations

The result is a data-based ranking, not a guarantee of future outcomes. The model does not currently include injuries, roster changes, venue conditions, matchups, or uncertainty estimates. Its weights are manually selected and supported by exploratory charts rather than learned and validated against a separate set of historical match results.
