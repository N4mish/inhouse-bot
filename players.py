# players.py
# Authored by Kashif Bandali 6/17


class Player:
    role_prefs = [] # Empty list of role prefs, will be populated when player constructed

    # Constructor to create the player
    def __init__(self, ign: str, rank: str, role_prefs: list[str]) -> None:
        self.ign = ign
        self.rank = rank
        self.role_prefs = role_prefs
    
    # Function that returns the role preferences of a specific plaer
    def get_prefs(self) -> list[str]:
        return self.role_prefs
    
    # Function that sets the mmr of a specific player
    def set_mmr(self, mmr: int) -> None:
        self.mmr = mmr