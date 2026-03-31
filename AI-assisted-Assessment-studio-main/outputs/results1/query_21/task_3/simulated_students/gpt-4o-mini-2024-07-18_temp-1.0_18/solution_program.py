import os

class BoardGame:
    def __init__(self):
        self.players = {}
        self.load_players()

    def load_players(self):
        if os.path.exists('players.txt'):
            with open('players.txt', 'r') as f:
                for line in f:
                    name, score = line.strip().split(',')
                    self.players[name] = int(score)

    def save_players(self):
        with open('players.txt', 'w') as f:
            for name, score in self.players.items():
                f.write(f'{name},{score}\n')

    def add_player(self, name, initial_score):
        if name not in self.players:
            self.players[name] = initial_score
            self.save_players()

    def update_score(self, name, points):
        if name in self.players:
            self.players[name] += points
            self.save_players()

    def get_highest_score(self):
        if self.players:
            highest_player = max(self.players.items(), key=lambda item: item[1])[0]
            return highest_player
        return None