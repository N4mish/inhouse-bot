# sort.py
# Authored by Kashif Bandali 6/17/23
# Purpose: 

# Import statements
from players import Player
import random

# Data structures
ranks = {"iron": 1, "bronze": 2, "silver": 3, "gold": 5, "platinum": 7, "diamond": 9, "master": 11, "grandmaster": 13, "challenger": 15}

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
    
# Function that returns a dictionary mapping each role to their respective player
# Inputs: A dictionary (dict{str:list[str]})
# REMEMBER: OPTIMAL FOR THE PARTY OFFERING THE MATCH
def gale_shapley(playerPref, rankPref) -> dict:
    # Iterate through the list of roles...

    pass

if __name__ == "__main__": # when you run the program --> runs this statement
    # for player in players:
    #     calculate_mmr(player)
    #     print(player.ign + ": " + str(player.rank) + ", " + str(player.mmr))
    # Some hardcode for now that sets players mmr:
    for player in players:
        player.mmr = ranks[player.rank]
    #sorting_time()