class ScoreCard:
    def __init__(self, players):
        self.scores = {}
        for player in players:
            self.scores[player] = 0

    def add_score(self, player, points):
        if player in self.scores:
            self.scores[player] += points

    def get_score(self, player):
        if player in self.scores:
            return self.scores[player]
        return None

    def get_winner(self):
        max_score = max(self.scores.values())
        for player in self.scores:
            if self.scores[player] == max_score:
                return player
        return None
