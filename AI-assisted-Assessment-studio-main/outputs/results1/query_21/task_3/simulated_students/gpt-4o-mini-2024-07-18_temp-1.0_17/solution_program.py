import os

class BoardGame:
    def __init__(self):
        self.players = {}
        self.filename = 'players.txt'
        self.load_players()

    def load_players(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                for line in f:
                    name, score = line.strip().split(',')
                    self.players[name] = int(score)

    def save_players(self):
        with open(self.filename, 'w') as f:
            for name, score in self.players.items():
                f.write(f'{name},{score}\n')

    def add_player(self, name, initial_score):
        self.players[name] = initial_score
        self.save_players()

    def update_score(self, name, points):
        if name in self.players:
            self.players[name] += points
            self.save_players()

    def get_highest_score(self):
        if not self.players:
            return None
        highest_score_player = max(self.players.items(), key=lambda x: (x[1], -list(self.players.keys()).index(x[0])))[0]
        return highest_score_player