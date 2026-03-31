class BoardGame:
    def __init__(self):
        self.players = []

    def add_player(self, player_name):
        player_name = player_name.lower()
        if player_name not in self.players:
            self.players.append(player_name)

    def remove_player(self, player_name):
        player_name = player_name.lower()
        if player_name in self.players:
            self.players.remove(player_name)

    def get_players(self):
        if not self.players:
            return "No players"
        return ", ".join([player.capitalize() for player in self.players])