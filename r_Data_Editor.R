library(tidyverse)
library(snakecase)

# CHANGE FILE INPUTS AND OUTPUTS NEXT TIME
# Note that everything is set for 2021. 

# Read in Data, retain column names currently developed in Python
df <- read.table("cbb_DataR.txt", sep = '\t', quote = "", header = TRUE, check.names = FALSE)

# Create dataframe with teams organized by their game index. Reverse order of rows of each game.
# This will give us a column to merge to the data which provides the opponent for each team listed.
df_opp <- df %>% group_by(gameIndex) %>% select(Teams) %>% map_df(rev)

# Ungroup for later.
df_opp <- ungroup(df_opp)

# Provide column names to df_opp
colnames(df_opp) <- c("gameIndex", "Opponent")

# Sort by gameIndex 
df_opp <- df_opp[order(df_opp$gameIndex),]

# Add Opponent column and drop extra gameIndex column
df2 <- cbind(df, df_opp %>% select(-gameIndex))


# Adding Opponent column after Team column for visual ease.
df2 <- df2 %>% relocate(Opponent, .after = Teams)

# Adding Historical Averages leading up to a matchup.
df2 <- df2 %>% group_by(Teams) %>% mutate(coverHist = lag(coverHist),
                                          coverDiffHist = lag(coverDiff),
                                          avgH1Hist = lag(cummean(`1`)),
                                          avgH2Hist = lag(cummean(`2`)),
                                          avgTHist = lag(cummean(`T`)),
                                          avgFieldGoalHist = lag(cummean(`Field Goal %`)),
                                          avgThreePointHist = lag(cummean(`Three Point %`)),
                                          avgFreeThrowHist = lag(cummean(`Free Throw %`)),
                                          avgReboundHist = lag(cummean(Rebounds)),
                                          avgOffensiveReboundsHist = lag(cummean(`Offensive Rebounds`)),
                                          avgDefensiveReboundsHist = lag(cummean(`Defensive Rebounds`)),
                                          avgAssistsHist = lag(cummean(Assists)),
                                          avgStealsHist = lag(cummean(Steals)),
                                          avgBlocksHist = lag(cummean(Blocks)),
                                          avgTotalTurnoversHist = lag(cummean(`Total Turnovers`)),
                                          avgFoulsHist = lag(cummean(Fouls)),
                                          avgSpreadHist = lag(cummean(Spread)))

# Format Column Names:
colnames(df2) <- snakecase::to_lower_camel_case(colnames(df2))
colnames(df2)[c(3,4)] <- c("h1","h2")

# Overwrite cbb_DataEdit
write.table(df2,"cbb_DataProcessed.txt", sep = '\t')
write.csv(df2, "cbb_DataProcessed.csv")

# Delete old data file no longer needed in directory.
file.remove("cbb_DataR.txt")
