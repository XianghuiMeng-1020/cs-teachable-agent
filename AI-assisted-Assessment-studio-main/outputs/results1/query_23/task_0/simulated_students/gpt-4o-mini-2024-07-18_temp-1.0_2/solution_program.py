class BoardGame:
    def __init__(self):
        self.player_scores = {}

    def add_player(self, player_name):
        self.player_scores[player_name] = []

    def record_score(self, player_name, score):
        self.player_scores[player_name].append(score)

    def get_player_total_score(self, player_name):
        return sum(self.player_scores[player_name])

    def get_winner(self):
        max_score = -1
        winner = None
        for player, scores in self.player_scores.items():
            total_score = sum(scores)
            if total_score > max_score:
                max_score = total_score
                winner = player
            elif total_score == max_score:
                if winner is None or player < winner:
                    winner = player
        return winner