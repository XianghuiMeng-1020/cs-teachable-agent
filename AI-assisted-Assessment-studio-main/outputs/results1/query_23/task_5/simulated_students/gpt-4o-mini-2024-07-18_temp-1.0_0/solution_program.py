class ScoreCard:
    def __init__(self, players):
        self.scores = {player: 0 for player in players}
        self.order = {player: index for index, player in enumerate(players)}

    def add_score(self, player, points):
        if player in self.scores:
            self.scores[player] += points

    def get_score(self, player):
        return self.scores.get(player, None)

    def get_winner(self):
        max_score = max(self.scores.values())
        winners = [player for player, score in self.scores.items() if score == max_score]
        return sorted(winners, key=lambda x: self.order[x])[0]