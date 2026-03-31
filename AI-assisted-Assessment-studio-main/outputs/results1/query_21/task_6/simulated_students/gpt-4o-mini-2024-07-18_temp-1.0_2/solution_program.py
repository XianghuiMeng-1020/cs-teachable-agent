import os

class BoardGameScoreboard:
    def __init__(self, filename):
        self.filename = filename
        self.scores = {}
        self.load_scores()

    def load_scores(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    if ':' in line:
                        player_name, score = line.strip().split(':')
                        self.scores[player_name] = self.scores.get(player_name, 0) + int(score)

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