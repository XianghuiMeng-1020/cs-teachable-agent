class Scoreboard:
    def __init__(self, player_names):
        self.scores = {name: 0 for name in player_names}

    def update_score(self, player_name, score_change):
        if player_name in self.scores:
            self.scores[player_name] += score_change

    def get_score(self, player_name):
        return self.scores.get(player_name, None)

    def get_winner(self):
        max_score = max(self.scores.values())
        winners = [name for name, score in self.scores.items() if score == max_score]
        return ', '.join(sorted(winners))

    def get_all_scores(self):
        sorted_scores = sorted(self.scores.items())
        return ', '.join([f'{name}:{score}' for name, score in sorted_scores])