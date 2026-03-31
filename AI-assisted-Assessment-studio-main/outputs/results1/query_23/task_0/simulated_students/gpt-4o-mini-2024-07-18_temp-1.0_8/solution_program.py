class BoardGame:
    def __init__(self):
        self.scores = {}

    def add_player(self, player_name):
        self.scores[player_name] = []

    def record_score(self, player_name, score):
        self.scores[player_name].append(score)

    def get_player_total_score(self, player_name):
        return sum(self.scores[player_name])

    def get_winner(self):
        winner = max(self.scores, key=lambda player: (self.get_player_total_score(player), -ord(player[0])))
        return winner