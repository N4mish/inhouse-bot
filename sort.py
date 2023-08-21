# sort.py
# Authored by Kashif Bandali 6/17/23
# Purpose: 

# Import statements
from players import Player
import random

# Data structures
ranks = {"iron": 1, "bronze": 2, "silver": 3, "gold": 5, "platinum": 7, "emerald": 9, "diamond": 11, "master": 13, "grandmaster": 15, "challenger": 17}

# Create a bunch of players
kashif = Player("ogopa", "diamond", ["MID", "SUP", "JNG", "ADC", "TOP"])
teresa = Player("bubbiextea", "silver", ["MID", "SUP", "ADC", "TOP", "JNG"])
namish = Player("a snowy night", "platinum", ["JNG", "SUP", "TOP", "MID", "ADC"])
sahand = Player("playernumber6", "master", ["TOP", "SUP", "ADC", "MID", "JNG"])
obama = Player("baracktheg0at", "iron", ["MID", "ADC", "JNG", "SUP", "TOP"])
players = [kashif, teresa, namish, sahand, obama]

# Function that calcultes each player's "mmr"
# Inputs: A player
# Outputs: None (sets the player's mmr internally)
def calculate_mmr(player: Player) -> None:
    base = random.randint(1, 10) # Element of randomness
    player.set_mmr(base * ranks[player.rank])


# Function that splits 10 people into two fair teams of 5
# Inputs: A list of 10 players
# Output: A red team and a blue team


# Function that returns a dictionary mapping each role to their respective player
# Inputs: A dictionary (dict{str:list[str]})
# REMEMBER: OPTIMAL FOR THE PARTY OFFERING THE MATCH
def gale_shapley(players) -> dict:
    # Psuedocode...
    # Put all the players in a queue (playerQueue)
    # For each player (p0), while they are unmatched, offer a match to their highest priority role (d0) that has not gotten an offer from them before
    #   Case 1: If the role does not already have a match, instant accept
    #   Case 2: If the role already has a match (p1), then check its preferences to see if it prefers the new offer
    #       If the role prefers its current match (p1) over this one (p0), then reject the match and add the player to the end of the queue (p0 --> end)
    #       If the role prefers this player (p) over its current match (p1), accept the new player and add the old player to the end of the queue (p1 --> end)
    # Repeat until there are no hospitals left in the queue

    # Variables needed: The preference list of the players, the preference list of the hospitals

    # (1) Sort the players in reverse mmr
    sorted_players = sorted(players, key=lambda player: player.mmr)

    # TEMP (2) Set the preference list of all the ranks to this list
    rank_pref = {"TOP": None, "JNG": None, "MID": None, "ADC": None, "SUP": None}
    for i in rank_pref:
        i



    # Iterate through the list of roles...
    return None

if __name__ == "__main__": # when you run the program --> runs this statement
    # for player in players:
    #     calculate_mmr(player)
    #     print(player.ign + ": " + str(player.rank) + ", " + str(player.mmr))
    # Some hardcode for now that sets players mmr:
    for player in players:
        player.mmr = ranks[player.rank]
    temp = gale_shapley(players)
    #sorting_time()