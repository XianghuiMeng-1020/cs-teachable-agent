import os

class BoardGame:
    def __init__(self):
        self.players = {}
        self.load_players()

    def load_players(self):
        if os.path.exists('players.txt'):
            with open('players.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split(',')
                    self.players[name] = int(score)

    def save_players(self):
        with open('players.txt', 'w') as file:
            for name, score in self.players.items():
                file.write(f'{name},{score}\n')

    def add_player(self, name, initial_score):
        if name not in self.players:
            self.players[name] = initial_score
            self.save_players()

    def update_score(self, name, points):
        if name in self.players:
            self.players[name] += points
            self.save_players()

    def get_highest_score(self):
        if not self.players:
            return None
        highest_score = max(self.players.values())
        for name in self.players:
            if self.players[name] == highest_score:
                return name