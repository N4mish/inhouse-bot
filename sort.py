# sort.py
# Authored by Kashif Bandali 6/17/23
# Purpose: 

# Import statements
from players import Player
from collections import deque
import random

# Data structures
ranks = {"iron": 1, "bronze": 2, "silver": 3, "gold": 5, "platinum": 7, "emerald": 9, "diamond": 11, "master": 13, "grandmaster": 15, "challenger": 17}

# Create a bunch of players (hardcode)
kashif = Player("ogopa", "diamond", ["MID", "SUP", "JNG", "ADC", "TOP"])
teresa = Player("bubbiextea", "silver", ["MID", "SUP", "ADC", "TOP", "JNG"])
namish = Player("a snowy night", "platinum", ["JNG", "SUP", "TOP", "MID", "ADC"])
sahand = Player("playernumber6", "master", ["TOP", "SUP", "ADC", "MID", "JNG"])
obama = Player("baracktheg0at", "iron", ["MID", "ADC", "JNG", "SUP", "TOP"])

becca = Player("guccye", "gold", ["SUP", "MID", "ADC", "TOP", "JNG"])
raymond = Player("looksmaxxer", "grandmaster", ["MID", "JNG", "TOP", "SUP", "ADC"])
alex = Player("asexian", "platinum", ["ADC", "SUP", "TOP", "JNG", "MID"])
dasol = Player("dasol", "master", ["ADC", "MID", "TOP", "JNG", "SUP"])
jason = Player("ssun", "grandmaster", ["MID", "TOP", "JNG", "SUP", "ADC"])
players = [kashif, teresa, namish, sahand, obama, becca, raymond, alex, dasol, jason]

'''
# Function that calcultes each player's "mmr"
# Inputs: A player
# Outputs: None (sets the player's mmr internally)
'''
def calculate_mmr(player: Player) -> None:
    base = random.randint(1, 10) # Element of randomness
    player.set_mmr(base * ranks[player.rank])

'''
# Function returns the ranking of an item in a player's list
# Inputs: A list of preferencs and the item of which index to return
# Outputs: Index of the preference
'''
def get_index(preferences, item):
    for i in range(len(preferences)):
        if preferences[i] == item: return i
    return None

'''
# Function that splits 10 people into two fair teams of 5
# Inputs: A list of 10 players
# Output: A red team and a blue team
'''
def split_teams(players) -> list[players]:
    salt = random.randint(0,1)
    sorted_players = sorted(players, key=lambda player: player.mmr)
    for i in sorted_players:
        print(i.ign)
    print("")
    blue = [sorted_players[0], sorted_players[2], sorted_players[4], sorted_players[7], sorted_players[9]]
    red = [sorted_players[1], sorted_players[3], sorted_players[5], sorted_players[6], sorted_players[8]]
    if salt == 0:
        blue = [sorted_players[1], sorted_players[3], sorted_players[5], sorted_players[6], sorted_players[8]]
        red = [sorted_players[0], sorted_players[2], sorted_players[4], sorted_players[7], sorted_players[9]]
    return ([blue, red])

'''
# Function that returns a dictionary mapping each role to their respective player
# Inputs: A dictionary (dict{str:list[str]})
# REMEMBER: OPTIMAL FOR THE PARTY OFFERING THE MATCH
'''
def gale_shapley(players) -> dict:
    # Psuedocode...
    # Put all the players in a queue (playerQueue)
    # For each player (p0), while they are unmatched, offer a match to their highest priority role (d0) that has not gotten an offer from them before
    #   Case 1: If the role does not already have a match, instant accept
    #   Case 2: If the role already has a match (p1), then check its preferences to see if it prefers the new offer
    #       If the role prefers its current match (p1) over this one (p0), then reject the match and add the player to the end of the queue (p0 --> end)
    #       If the role prefers this player (p) over its current match (p1), accept the new player and add the old player to the end of the queue (p1 --> end)
    # Repeat until there are no hospitals left in the queue

    # Variables needed: The preference list of the players, the preference list of the hospitals, the list of matches
    matches = {"TOP": None, "JNG": None, "MID": None, "ADC": None, "SUP": None}
    # (1) Sort the players in reverse mmr
    sorted_players = sorted(players, key=lambda player: player.mmr)

    # (2) Set the preference list of all the ranks to this list
    rank_pref = {"TOP": None, "JNG": None, "MID": None, "ADC": None, "SUP": None}
    for i in rank_pref:
        rank_pref[i] = sorted_players

    # (3) Store the index of player preference that we are on
    pref_index = {}
    for player in sorted_players:
        pref_index[player] = 0

    # (4) Create a queue with all the players
    queue = deque()
    for i in sorted_players:
        queue.append(i)

    # Iterate through the list of players...
    # print(f"matches are {matches}")
    # print(f"rank prefs are {rank_pref}")
    # print(f"pref index is {pref_index}")

    while(len(queue) != 0):
        # pop off top player in queue
        # debugging the queue:
        p0 = queue.popleft()
        r0 = p0.role_prefs[pref_index[p0]]
        pref_index[p0] += 1 # increment the index of p0's preference list
        # (1) Check if r0 is free
        if matches[r0] == None:
            matches[r0] = p0 # match :D
        else:
        # (2) If r0 is not free... then it is currently matched to p1
            p1 = matches[r0]
            # (a) If r0 prefers new p0 > p1 --> SWAP
            if get_index(rank_pref[r0], p0) < get_index(rank_pref[r0], p1):
                # swap
                matches[r0] = p0
                queue.append(p1)
            # (b) Otherwise, r0 prefers its current match p1 > p0 (just add back to queue)
            else:
                queue.append(p0)
    return matches

if __name__ == "__main__": # when you run the program --> runs this statement
    # for player in players:
    #     calculate_mmr(player)
    #     print(player.ign + ": " + str(player.rank) + ", " + str(player.mmr))
    # Some hardcode for now that sets players mmr:
    for player in players:
        player.mmr = ranks[player.rank]
    temp = split_teams(players)
    print("blue team is")
    for i in temp[0]:
        print(i.ign)
    print("red team is")
    for i in temp[1]:
        print(i.ign)
    
    blue = gale_shapley(temp[0])
    red = gale_shapley(temp[1])

    for role in blue:
        print(f"Role {role} is assigned to {blue[role].ign}.")
    
    print(" ")
    
    for role in red:
        print(f"Role {role} is assigned to {red[role].ign}.")

    #sorting_time()