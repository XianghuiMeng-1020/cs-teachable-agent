class BoardGame:
    def __init__(self, name, players, status):
        self.name = name.lower()
        self.players = [player.lower() for player in players]
        self.status = status.lower()

    def add_player(self, player_name):
        player_name = player_name.lower()
        if self.status == 'ongoing' and player_name not in self.players:
            self.players.append(player_name)

    def remove_player(self, player_name):
        player_name = player_name.lower()
        if player_name in self.players:
            self.players.remove(player_name)

    def finish_game(self):
        self.status = 'completed'

    def game_summary(self):
        player_count = len(self.players)
        players_list = ', '.join(self.players)
        return f'Game: {self.name}, Players: {player_count}, List: [{players_list}], Status: {self.status}'