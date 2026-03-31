class BoardGame:
    def __init__(self):
        self.players = []

    def add_player(self, player_name):
        if player_name.lower() not in [p.lower() for p in self.players]:
            self.players.append(player_name)

    def remove_player(self, player_name):
        self.players = [p for p in self.players if p.lower() != player_name.lower()]

    def get_players(self):
        if not self.players:
            return "No players"
        return ', '.join(self.players)