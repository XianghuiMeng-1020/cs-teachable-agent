class BoardGame:
    def __init__(self, name, players, status):
        self.name = name.lower()
        self.players = [player.lower() for player in players]
        self.status = status.lower()

    def add_player(self, player):
        if self.status == 'ongoing' and player.lower() not in self.players:
            self.players.append(player.lower())

    def remove_player(self, player):
        if player.lower() in self.players:
            self.players.remove(player.lower())

    def finish_game(self):
        self.status = 'completed'

    def game_summary(self):
        players_formatted = ', '.join(self.players)
        return f"Game: {self.name}, Players: {len(self.players)}, List: [{players_formatted}], Status: {self.status}"