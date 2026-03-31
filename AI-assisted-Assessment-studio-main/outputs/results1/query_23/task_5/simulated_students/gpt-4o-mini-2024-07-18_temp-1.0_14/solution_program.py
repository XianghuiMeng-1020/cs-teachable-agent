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
        max_score = -1
        winner = None
        for player in self.scores:
            if self.scores[player] > max_score:
                max_score = self.scores[player]
                winner = player
            elif self.scores[player] == max_score:
                if winner is None or self.order[player] < self.order[winner]:
                    winner = player
        return winner