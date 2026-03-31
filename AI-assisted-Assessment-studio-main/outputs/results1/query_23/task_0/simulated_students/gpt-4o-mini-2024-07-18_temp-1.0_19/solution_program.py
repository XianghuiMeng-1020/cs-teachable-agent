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
        max_score = -1
        winner = None
        for player, score in self.scores.items():
            total_score = sum(score)
            if total_score > max_score or (total_score == max_score and player < winner):
                max_score = total_score
                winner = player
        return winner