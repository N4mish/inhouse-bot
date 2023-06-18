# players.py
# Authored by Kashif Bandali 6/17


class Player:
    role_prefs = {}
    def __init__(self, rank, role_prefs):
        self.rank = rank
        self.role_prefs = role_prefs
    
    def get_prefs(self):
        return self.role_prefs