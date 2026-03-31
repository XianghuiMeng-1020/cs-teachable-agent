class BoardGame:
    def __init__(self):
        self.scores = {}

    def add_player(self, player_name):
        self.scores[player_name] = []

    def record_score(self, player_name, score):
        if player_name in self.scores:
            self.scores[player_name].append(score)

    def get_player_total_score(self, player_name):
        if player_name in self.scores:
            return sum(self.scores[player_name])
        return 0

    def get_winner(self):
        total_scores = {player: sum(scores) for player, scores in self.scores.items()}
        max_score = max(total_scores.values())
        winners = [player for player, score in total_scores.items() if score == max_score]
        return sorted(winners)[0]