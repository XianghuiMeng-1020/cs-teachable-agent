import os

class BoardGameScoreboard:
    def __init__(self, filename):
        self.filename = filename
        self.scores = {}
        if os.path.exists(self.filename):
            self.load_scores()
        else:
            self.save_scores()  

    def add_score(self, player_name, score):
        if player_name in self.scores:
            self.scores[player_name] += score
        else:
            self.scores[player_name] = score
        self.save_scores()

    def get_score(self, player_name):
        return self.scores.get(player_name, 0)

    def save_scores(self):
        with open(self.filename, 'w') as f:
            for player, score in self.scores.items():
                f.write(f'{player}:{score}\n')

    def load_scores(self):
        with open(self.filename, 'r') as f:
            for line in f:
                player, score = line.strip().split(':')
                self.scores[player] = int(score)