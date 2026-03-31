class BoardGame:
    def __init__(self, name, players, status):
        self.name = name.lower()
        self.players = [player.lower() for player in players]
        self.status = status.lower()

    def add_player(self, player):
        player = player.lower()
        if self.status == 'ongoing' and player not in self.players:
            self.players.append(player)

    def remove_player(self, player):
        player = player.lower()
        if player in self.players:
            self.players.remove(player)

    def finish_game(self):
        self.status = 'completed'

    def game_summary(self):
        player_count = len(self.players)
        players_list = ', '.join(self.players)
        return f"Game: {self.name}, Players: {player_count}, List: [{players_list}], Status: {self.status}"