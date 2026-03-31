class Leaderboard:
    def __init__(self):
        self.scores = {}

    def add_player(self, player_name):
        if player_name not in self.scores:
            self.scores[player_name] = 0

    def update_score(self, player_name, score):
        if player_name in self.scores:
            self.scores[player_name] += score
        else:
            self.scores[player_name] = score

    def get_score(self, player_name):
        return self.scores.get(player_name, None)

    def save_scores(self, filepath):
        with open(filepath, 'w') as file:
            for player_name, score in self.scores.items():
                file.write(f'{player_name}:{score}\n')

    def load_scores(self, filepath):
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    player_name, score = line.strip().split(':')
                    self.scores[player_name] = int(score)
        except FileNotFoundError:
            pass
