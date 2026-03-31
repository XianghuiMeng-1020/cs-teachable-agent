class BoardGame:
    def __init__(self):
        self.players_scores = {}

    def add_player(self, player_name):
        self.players_scores[player_name] = []

    def record_score(self, player_name, score):
        self.players_scores[player_name].append(score)

    def get_player_total_score(self, player_name):
        return sum(self.players_scores[player_name])

    def get_winner(self):
        winner = max(self.players_scores, key=lambda p: (sum(self.players_scores[p]), p))
        return winner