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
        total_scores = {player: self.get_player_total_score(player) for player in self.players_scores}
        winner = max(total_scores.items(), key=lambda x: (x[1], x[0]))
        return winner[0]