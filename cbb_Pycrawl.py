#### Scrape ESPN

import requests
import time
from bs4 import BeautifulSoup
import re
from datetime import date, timedelta
import json
from tqdm import tqdm
import os
from global_ import priorRunBoolean

#Put path here
#os.chdir(r'')

#If this script was previously ran, ensure that we saved the number of links
#pulled on the last run.

try:
    
    #Assert True
    assert(priorRunBoolean)
    
    with open("cbb_Links.json", "r") as f:
        jsonLinks = json.load(f)
        count = len(jsonLinks)
    
    print(f"Previous run found. Last link total at {count}. Saving count to .txt file.")
    
    with open("last_run_count.txt", "w") as f:
        f.write(str(count))
    
    
except:
    print("No prior run found. Current run will estabilish new count and save file at end of script.")
    
    
        

# Get required dates.
start_season = date(2022, 11, 7) # ONLY CHANGE TO NEW SEASON
current_date =  date.today()
time_step = timedelta(days=1)

# Initialize

links = []
dates = []

# While Loop - While the date is less than or equal to current date, add the formatted date to the list.
# The second line just means add a day until the loop is over.
while start_season <= current_date:
    dates.append(start_season.strftime("%Y%m%d"))
    start_season += time_step 
    
# Read Links on ESPN's scorebord webpage by day (represented by i)

for i in tqdm(range(len(dates))):
 response = requests.get(f"https://www.espn.com/mens-college-basketball/scoreboard/_/date/{dates[i]}/group/50") # Links are organized by date.
 soup = BeautifulSoup(response.text, "html.parser") # Get HTML portions of these webpages.

 # Find Links That we want.
 internal_links = [link["href"] for link in soup.find_all("a", href=True) if "/game/_/gameId" in link["href"]] #For tags with href in html text, internal links equals the ones with the "/game..." pattern present
 internal_links = [re.sub(r"game/", "matchup/", link) for link in internal_links] # Replace the "game/" part of each link string with "matchup/"... this will lead us to the stats of each game
 links.extend(internal_links)


 time.sleep(1) # So we don't bother ESPN's servers too much

links = ["https://www.espn.com" + link for link in links]

with open("cbb_Links.json", "w") as game_links: # Save JSON File
    json.dump(links, game_links)
     
#Save File denoting the count of links pulled prior to run:
if priorRunBoolean == False:
    with open("last_run_count.txt", "w") as f:
        f.write(str(len(links)))