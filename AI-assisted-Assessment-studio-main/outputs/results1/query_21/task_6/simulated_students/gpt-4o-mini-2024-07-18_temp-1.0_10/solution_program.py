import os

class BoardGameScoreboard:
    def __init__(self, filename):
        self.filename = filename
        self.scores = {}
        self.load_scores()

    def create_scoreboard(self):
        with open(self.filename, 'w') as file:
            pass  # Create an empty file

    def load_scores(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    player, score = line.strip().split(':')
                    self.scores[player] = self.scores.get(player, 0) + int(score)

    def save_scores(self):
        with open(self.filename, 'w') as file:
            for player, score in self.scores.items():
                file.write(f'{player}:{score}\n')

    def add_score(self, player_name, score):
        self.scores[player_name] = self.scores.get(player_name, 0) + score
        self.save_scores()

    def get_score(self, player_name):
        return self.scores.get(player_name, 0)