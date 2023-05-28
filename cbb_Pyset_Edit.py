import os
import pandas as pd
import rpy2.robjects as robjects

os.getcwd()

df = pd.read_csv("cbb_DataRaw.txt", sep = '\t').drop_duplicates()

# Specify whether a team covered or not
def covered(row):
    if row['Teams'] == row['Favored Team'] and row['T'] <= -row['Spread']:
        value = 0
    elif row['Teams'] == row['Favored Team'] and row['T'] > -row['Spread']:
        value = 1
    elif row['Teams'] != row['Favored Team'] and row['T'] > 0:
        value = 1
    elif  row['Teams'] != row['Favored Team'] and row['T'] > -row['Spread']:
        value = 1
    else:
        value = 0
    return value

# Function that says, by row, which team is favored (numerically; 1 or 0)
def favored(row):
    if row['Teams'] == row['Favored Team']:
        value = 1
    else:
        value = 0
    return value

# This function takes the cumulative cover success differences between opponents in a matchup
def cover_diff(row):
    row1val = row['coverHist'].iloc[0] - row['coverHist'].iloc[1]
    row2val = row['coverHist'].iloc[1] - row['coverHist'].iloc[0]
    return(row1val, row2val)


# Apply Cover and Cumulative Cover Results
df["covered"] = df.apply(covered, axis=1)
df["coverHist"] = df.groupby('Teams')['covered'].transform(pd.Series.cumsum)
df['favored'] = df.apply(favored, axis = 1)


df["gameIndex"] = [i for i in range(1, int(len(df.index)/2+1)) for _ in range(2)] # Create Game ID index

# Let's Get Cumulative Spread performance differences per game
df['covDiff1'] =  df.groupby('gameIndex')["coverHist"].diff()
df['covDiff2'] =  df.groupby('gameIndex')["coverHist"].diff(periods = -1)
df['coverDiff'] = df['covDiff1'].fillna(df['covDiff2'] )
df.drop(['covDiff1', 'covDiff2'], axis = 1, inplace=True)

# Averaged Stuffs
df_means = df.drop(['coverHist', 'Flagrant Fouls', 'gameIndex'], axis = 1).groupby('Teams').mean()
df_means['Teams'] =  df_means.index

df.to_csv("cbb_DataR.txt", sep = '\t', header = True, index = False)

# Call R script to get opponents column and historical averages
r =  robjects.r
r.source('r_Data_Editor.R')


