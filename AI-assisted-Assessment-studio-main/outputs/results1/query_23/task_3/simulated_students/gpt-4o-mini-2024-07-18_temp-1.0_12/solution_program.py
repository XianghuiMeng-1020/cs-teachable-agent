class BoardGame:
    def __init__(self):
        self.players = []

    def add_player(self, player_name):
        player_name = player_name.lower()
        if player_name not in (p.lower() for p in self.players):
            self.players.append(player_name)

    def remove_player(self, player_name):
        player_name = player_name.lower()
        self.players = [p for p in self.players if p.lower() != player_name]

    def get_players(self):
        if self.players:
            return ', '.join(self.players)
        else:
            return 'No players'