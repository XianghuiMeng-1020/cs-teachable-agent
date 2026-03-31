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
        if player in self.scores:
            return self.scores[player]
        return None

    def get_winner(self):
        if not self.scores:
            return None
        max_score = max(self.scores.values())
        for player in self.order:
            if self.scores[player] == max_score:
                return player
        return None