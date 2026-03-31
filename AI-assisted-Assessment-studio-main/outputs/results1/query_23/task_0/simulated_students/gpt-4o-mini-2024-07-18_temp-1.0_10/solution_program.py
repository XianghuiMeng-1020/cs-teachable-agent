class BoardGame:
    def __init__(self):
        self.players_scores = {}

    def add_player(self, player_name):
        self.players_scores[player_name] = []

    def record_score(self, player_name, score):
        if player_name in self.players_scores:
            self.players_scores[player_name].append(score)

    def get_player_total_score(self, player_name):
        if player_name in self.players_scores:
            return sum(self.players_scores[player_name])
        return 0

    def get_winner(self):
        max_score = -1
        winner = None
        for player, scores in self.players_scores.items():
            total_score = sum(scores)
            if total_score > max_score:
                max_score = total_score
                winner = player
            elif total_score == max_score:
                winner = min(winner, player)
        return winner