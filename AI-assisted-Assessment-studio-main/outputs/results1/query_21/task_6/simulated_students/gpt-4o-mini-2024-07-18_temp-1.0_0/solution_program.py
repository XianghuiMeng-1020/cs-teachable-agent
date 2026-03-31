import os

class BoardGameScoreboard:
    def __init__(self, file_name):
        self.file_name = file_name
        self.scores = {}
        self.load_scores()

    def load_scores(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                for line in file:
                    if ':' in line:
                        player_name, score = line.strip().split(':')
                        self.scores[player_name] = int(score)

    def save_scores(self):
        with open(self.file_name, 'w') as file:
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