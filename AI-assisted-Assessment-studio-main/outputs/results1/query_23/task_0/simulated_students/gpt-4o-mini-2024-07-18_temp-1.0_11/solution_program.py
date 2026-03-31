class BoardGame:
    def __init__(self):
        self.players = {}

    def add_player(self, player_name):
        self.players[player_name] = []

    def record_score(self, player_name, score):
        if player_name in self.players:
            self.players[player_name].append(score)

    def get_player_total_score(self, player_name):
        if player_name in self.players:
            return sum(self.players[player_name])
        return 0

    def get_winner(self):
        if not self.players:
            return None
        winner = max(self.players.items(), key=lambda item: (sum(item[1]), -ord(item[0][0])))[0]
        return winner