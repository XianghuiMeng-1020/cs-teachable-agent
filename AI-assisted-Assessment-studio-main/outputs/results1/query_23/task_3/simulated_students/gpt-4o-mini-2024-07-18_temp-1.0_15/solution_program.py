class BoardGame:
    def __init__(self):
        self.players = []

    def add_player(self, player_name):
        player_name_lower = player_name.lower()
        if not any(player.lower() == player_name_lower for player in self.players):
            self.players.append(player_name)

    def remove_player(self, player_name):
        player_name_lower = player_name.lower()
        self.players = [player for player in self.players if player.lower() != player_name_lower]

    def get_players(self):
        return ', '.join(self.players) if self.players else 'No players'