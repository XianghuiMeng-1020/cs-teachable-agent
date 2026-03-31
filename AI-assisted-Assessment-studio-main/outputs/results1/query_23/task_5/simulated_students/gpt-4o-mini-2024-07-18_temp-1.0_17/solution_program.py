class ScoreCard:
    def __init__(self, players):
        self.scores = {player: 0 for player in players}
        self.order = {player: idx for idx, player in enumerate(players)}

    def add_score(self, player, points):
        if player in self.scores:
            self.scores[player] += points

    def get_score(self, player):
        return self.scores.get(player, None)

    def get_winner(self):
        max_score = -1
        winner = None
        for player, score in self.scores.items():
            if score > max_score:
                max_score = score
                winner = player
            elif score == max_score:
                if self.order[player] < self.order[winner]:
                    winner = player
        return winner