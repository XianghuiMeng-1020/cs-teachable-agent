import json

class BoardGameScoreboard:
    def __init__(self, filename):
        self.filename = filename
        self.scores = {}
        self.load_scores()

    def load_scores(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    player_name, score = line.strip().split(':')
                    self.scores[player_name] = int(score)
        except FileNotFoundError:
            pass

    def save_scores(self):
        with open(self.filename, 'w') as file:
            for player_name, score in self.scores.items():
                file.write(f'{player_name}:{score}\n')

    def add_score(self, player_name, score):
        if player_name in self.scores:
            self.scores[player_name] += score
        else:
            self.scores[player_name] = score
        self.save_scores()

    def get_score(self, player_name):
        return self.scores.get(player_name, 0)