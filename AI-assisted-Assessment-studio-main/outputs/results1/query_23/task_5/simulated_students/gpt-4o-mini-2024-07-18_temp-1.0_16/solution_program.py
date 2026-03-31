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
        return self.scores.get(player)

    def get_winner(self):
        highest_score = -1
        winner = None
        for player in self.order:
            if self.scores[player] > highest_score:
                highest_score = self.scores[player]
                winner = player
        return winner