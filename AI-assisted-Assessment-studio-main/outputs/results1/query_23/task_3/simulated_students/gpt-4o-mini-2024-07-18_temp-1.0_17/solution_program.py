class BoardGame:
    def __init__(self):
        self.players = []

    def add_player(self, player_name):
        player_name = player_name.lower()
        if player_name not in (player.lower() for player in self.players):
            self.players.append(player_name)

    def remove_player(self, player_name):
        player_name = player_name.lower()
        self.players = [player for player in self.players if player.lower() != player_name]

    def get_players(self):
        if not self.players:
            return "No players"
        return ", ".join(self.players)