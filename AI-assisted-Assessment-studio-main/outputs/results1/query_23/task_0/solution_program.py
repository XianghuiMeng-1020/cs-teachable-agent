class BoardGame:
    def __init__(self):
        self.players = {}

    def add_player(self, player_name):
        if player_name not in self.players:
            self.players[player_name] = []

    def record_score(self, player_name, score):
        if player_name in self.players:
            self.players[player_name].append(score)

    def get_player_total_score(self, player_name):
        if player_name in self.players:
            return sum(self.players[player_name])
        return 0

    def get_winner(self):
        max_score = -1
        winner = None
        for player in self.players:
            total_score = self.get_player_total_score(player)
            if total_score > max_score:
                max_score = total_score
                winner = player
            elif total_score == max_score:
                if winner is not None and player < winner:
                    winner = player
        return winner
