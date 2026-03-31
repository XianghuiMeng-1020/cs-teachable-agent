class BoardGame:
    def __init__(self):
        self.player_scores = {}

    def add_player(self, player_name):
        self.player_scores[player_name] = []

    def record_score(self, player_name, score):
        if player_name in self.player_scores:
            self.player_scores[player_name].append(score)

    def get_player_total_score(self, player_name):
        return sum(self.player_scores[player_name])

    def get_winner(self):
        winner = None
        highest_score = -1
        for player, scores in self.player_scores.items():
            total_score = sum(scores)
            if total_score > highest_score or (total_score == highest_score and (winner is None or player < winner)):
                highest_score = total_score
                winner = player
        return winner