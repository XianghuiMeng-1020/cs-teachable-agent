class Scoreboard:
    def __init__(self, players):
        self.scores = {player: 0 for player in players}

    def update_score(self, player_name, score_change):
        if player_name in self.scores:
            self.scores[player_name] += score_change

    def get_score(self, player_name):
        return self.scores.get(player_name, 0)

    def get_winner(self):
        if not self.scores:
            return ""
        max_score = max(self.scores.values())
        winners = sorted([name for name, score in self.scores.items() if score == max_score])
        return ", ".join(winners)

    def get_all_scores(self):
        return ", ".join(f"{name}:{score}" for name, score in sorted(self.scores.items()))