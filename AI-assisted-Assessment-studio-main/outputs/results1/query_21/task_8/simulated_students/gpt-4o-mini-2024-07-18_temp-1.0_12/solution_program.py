class Leaderboard:
    def __init__(self):
        self.players = {}

    def add_player(self, player_name):
        if player_name not in self.players:
            self.players[player_name] = 0

    def update_score(self, player_name, score):
        if player_name in self.players:
            self.players[player_name] += score
        else:
            self.players[player_name] = score

    def get_score(self, player_name):
        return self.players.get(player_name, None)

    def save_scores(self, filepath):
        with open(filepath, 'w') as file:
            for player, score in self.players.items():
                file.write(f'{player}:{score}\n')

    def load_scores(self, filepath):
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    player, score = line.strip().split(':')
                    self.players[player] = int(score)
        except FileNotFoundError:
            pass