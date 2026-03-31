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
        max_score = max(total_scores.values())
        winners = [player for player, score in total_scores.items() if score == max_score]
        return sorted(winners)[0]