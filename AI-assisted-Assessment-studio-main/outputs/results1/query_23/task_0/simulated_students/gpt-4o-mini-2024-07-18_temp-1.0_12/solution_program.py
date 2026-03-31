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
        highest_score = -1
        winner = None
        for player_name, score_list in self.scores.items():
            total_score = sum(score_list)
            if total_score > highest_score:
                highest_score = total_score
                winner = player_name
            elif total_score == highest_score:
                winner = min(winner, player_name)
        return winner