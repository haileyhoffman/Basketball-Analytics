# from Team import *
from TeamStats import *
import re

from bs4 import BeautifulSoup
import urllib.request


data = []

soup = BeautifulSoup(urllib.request.urlopen("https://static.godrakebulldogs.com/custompages/Statistics/mbb-17-18/du-02.htm").read(), 'lxml')

#Scrapes the stats for the first half of the game
tbody = soup('table', {"style":"font-family:verdana;color:black;background:white;font-size:xx-small;text-align:right;"})[1].find_all('tr')

for col in tbody:
    rows = col.findChildren(recursive = False)
    rows = [ele.text.strip() for ele in rows]
    data.append(rows)


headers = data[0]



for x in headers:
    visitors_match = re.search("VISITORS: Drake", x)
    home_match = re.search("HOME TEAM: Drake", x)
    if visitors_match or home_match:
        break


if visitors_match:
    visiting_team = Team("Drake")

    players = []

    tbody2 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[0].find_all('tr', {"bgcolor": "#ffffff"})

    for col in tbody2:
        rows = col.findChildren(recursive=False)
        rows = [ele.text.strip() for ele in rows]
        players.append(rows)

    row_number = 0
    for row in players:
        match = re.search(r'TM', str(row))
        if match:
            break
        else:
            row_number += 1

    players = players[:row_number]

    for row in players:
        player_name = row[1]
        visiting_team.add_to_roster(PlayerStats(player_name))


    for row in players[0:5]:
        player_name = row[1]
        visiting_team.sub_in(player_name)


#####AUTOMATED#####
# elif headers[0] == "HOME TEAM: Drake":

elif home_match:
    home_team = Team("Drake")


    players = []

    tbody2 = soup('table', {"border": "0", "cellspacing": "0", "cellpadding": "2"})[1].find_all('tr', {"bgcolor": "#ffffff"})

    for col in tbody2:
        rows = col.findChildren(recursive=False)
        rows = [ele.text.strip() for ele in rows]
        players.append(rows)

    row_number = 0
    for row in players:
        match = re.search(r'TM', str(row))
        if match:
            break
        else:
            row_number += 1

    players = players[:row_number]

    for row in players:
        player_name = row[1]
        home_team.add_to_roster(PlayerStats(player_name))


    for row in players[0:5]:
        player_name = row[1]
        home_team.sub_in(player_name)


#####AUTOMATED#####
if visitors_match:
    visitingDictionary = {}
    visitingDictionary[visiting_team.get_tuple()] = TeamStats()

    for row in data:

        home = row[0]
        visitors = row[4]

        # entered game
        match = re.search(r'SUB IN : (.*)', str(visitors))
        if match:
            subin = match.group(1)
            visiting_team.sub_in(subin)

        # exited game
        match = re.search(r'SUB OUT: (.*)', str(visitors))
        if match:
            subout = match.group(1)
            visiting_team.sub_out(subout)

        # 2 pointer
        match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(visitors))
        if match:
            player = match.group(2)
            visiting5tuple = visiting_team.get_tuple()
            if not (visiting5tuple in visitingDictionary):
                visitingDictionary[visiting5tuple] = TeamStats()
            visitingDictionary[visiting5tuple].points_for += 2

        # FT
        match = re.search(r'GOOD! FT SHOT by (.*)', str(visitors))
        if match:
            player = match.group(1)
            visiting5tuple = visiting_team.get_tuple()
            if not (visiting5tuple in visitingDictionary):
                visitingDictionary[visiting5tuple] = TeamStats()
            visitingDictionary[visiting5tuple].points_for += 1

        # 3 Pointer
        match = re.search(r'GOOD! 3 PTR by (.*)', str(visitors))
        if match:
            player = match.group(1)
            visiting5tuple = visiting_team.get_tuple()
            if not (visiting5tuple in visitingDictionary):
                visitingDictionary[visiting5tuple] = TeamStats()
            visitingDictionary[visiting5tuple].points_for += 3

        # Fouls
        match = re.search(r'FOUL by (.*)', str(visitors))
        if match:
            player = match.group(1)
            visiting5tuple = visiting_team.get_tuple()
            if not (visiting5tuple in visitingDictionary):
                visitingDictionary[visiting5tuple] = TeamStats()
            visitingDictionary[visiting5tuple].Fouls_by_Team += 1

        # POINTS AGAINST
        # 2 pointer
        match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(home))
        if match:
            player = match.group(2)
            visiting5tuple = visiting_team.get_tuple()
            if not (visiting5tuple in visitingDictionary):
                visitingDictionary[visiting5tuple] = TeamStats()
            visitingDictionary[visiting5tuple].points_against += 2

        # FT
        match = re.search(r'GOOD! FT SHOT by (.*)', str(home))
        if match:
            player = match.group(1)
            visiting5tuple = visiting_team.get_tuple()
            if not (visiting5tuple in visitingDictionary):
                visitingDictionary[visiting5tuple] = TeamStats()
            visitingDictionary[visiting5tuple].points_against += 1

        # Fouls
        match = re.search(r'FOUL by (.*)', str(home))
        if match:
            player = match.group(1)
            visiting5tuple = visiting_team.get_tuple()
            if not (visiting5tuple in visitingDictionary):
                visitingDictionary[visiting5tuple] = TeamStats()
            visitingDictionary[visiting5tuple].Fouls_by_Opponent += 1

        # 3 Pointer
        match = re.search(r'GOOD! 3 PTR by (.*)', str(home))
        if match:
            player = match.group(1)
            visiting5tuple = visiting_team.get_tuple()
            if not (visiting5tuple in visitingDictionary):
                visitingDictionary[visiting5tuple] = TeamStats()
            visitingDictionary[visiting5tuple].points_against += 3


    for f in visitingDictionary.keys():
        print(f, visitingDictionary[f])


#####AUTOMATED#####
elif home_match:
    homeDictionary = {}
    homeDictionary[home_team.get_tuple()] = TeamStats()

    for row in data:

        home = row[0]
        visitors = row[4]

        #entered game
        match = re.search(r'SUB IN : (.*)', str(home))
        if match:
            subin = match.group(1)
            home_team.sub_in(subin)

        #exited game
        match = re.search(r'SUB OUT: (.*)', str(home))
        if match:
            subout = match.group(1)
            home_team.sub_out(subout)

        # 2 pointer
        match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(home))
        if match:
            player = match.group(2)
            home5tuple = home_team.get_tuple()
            if not (home5tuple in homeDictionary):
                homeDictionary[home5tuple] = TeamStats()
            homeDictionary[home5tuple].points_for +=2

        # FT
        match = re.search(r'GOOD! FT SHOT by (.*)', str(home))
        if match:
            player = match.group(1)
            home5tuple = home_team.get_tuple()
            if not (home5tuple in homeDictionary):
                homeDictionary[home5tuple] = TeamStats()
            homeDictionary[home5tuple].points_for += 1

        # Fouls
        match = re.search(r'FOUL by (.*)', str(home))
        if match:
            player = match.group(1)
            home5tuple = home_team.get_tuple()
            if not (home5tuple in homeDictionary):
                homeDictionary[home5tuple] = TeamStats()
            homeDictionary[home5tuple].Fouls_by_Team += 1
        # 3 Pointer
        match = re.search(r'GOOD! 3 PTR by (.*)', str(home))
        if match:
            player = match.group(1)
            home5tuple = home_team.get_tuple()
            if not (home5tuple in homeDictionary):
                homeDictionary[home5tuple] = TeamStats()
            homeDictionary[home5tuple].points_for += 3



    #POINTS AGAINST
        # 2 pointer
        match = re.search(r'GOOD! (DUNK|LAYUP|JUMPER) by (.*)', str(visitors))
        if match:
            player = match.group(2)
            home5tuple = home_team.get_tuple()
            if not (home5tuple in homeDictionary):
                homeDictionary[home5tuple] = TeamStats()
            homeDictionary[home5tuple].points_against +=2

        # FT
        match = re.search(r'GOOD! FT SHOT by (.*)', str(visitors))
        if match:
            player = match.group(1)
            home5tuple = home_team.get_tuple()
            if not (home5tuple in homeDictionary):
                homeDictionary[home5tuple] = TeamStats()
            homeDictionary[home5tuple].points_against += 1

        # 3 Pointer
        match = re.search(r'GOOD! 3 PTR by (.*)', str(visitors))
        if match:
            player = match.group(1)
            home5tuple = home_team.get_tuple()
            if not (home5tuple in homeDictionary):
                homeDictionary[home5tuple] = TeamStats()
            homeDictionary[home5tuple].points_against += 3

        # Fouls
        match = re.search(r'FOUL 3 PTR by (.*)', str(visitors))
        if match:
            player = match.group(1)
            home5tuple = home_team.get_tuple()
            if not (home5tuple in homeDictionary):
                homeDictionary[home5tuple] = TeamStats()
                homeDictionary[home5tuple].Fouls_by_Opponent += 1

    for f in homeDictionary.keys():
        print(f, homeDictionary[f])