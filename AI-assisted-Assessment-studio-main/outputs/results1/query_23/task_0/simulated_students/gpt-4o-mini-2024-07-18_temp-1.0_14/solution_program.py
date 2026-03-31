class BoardGame:
    def __init__(self):
        self.scores = {}

    def add_player(self, player_name):
        self.scores[player_name] = []

    def record_score(self, player_name, score):
        if player_name in self.scores:
            self.scores[player_name].append(score)

    def get_player_total_score(self, player_name):
        return sum(self.scores[player_name])

    def get_winner(self):
        highest_score = -1
        winners = []
        for player, scores in self.scores.items():
            total_score = sum(scores)
            if total_score > highest_score:
                highest_score = total_score
                winners = [player]
            elif total_score == highest_score:
                winners.append(player)
        return min(winners)