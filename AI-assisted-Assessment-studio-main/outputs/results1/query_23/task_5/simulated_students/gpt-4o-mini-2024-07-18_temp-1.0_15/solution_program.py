class ScoreCard:
    def __init__(self, players):
        self.scores = {player: 0 for player in players}
        self.order = []

    def add_score(self, player, points):
        if player in self.scores:
            self.scores[player] += points
            if player not in self.order:
                self.order.append(player)

    def get_score(self, player):
        return self.scores.get(player, None)

    def get_winner(self):
        if not self.scores:
            return None
        winner = None
        max_score = -1
        for player in self.order:
            if self.scores[player] > max_score:
                max_score = self.scores[player]
                winner = player
        return winner