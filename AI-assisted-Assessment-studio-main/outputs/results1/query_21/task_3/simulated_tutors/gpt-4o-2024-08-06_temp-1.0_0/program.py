# Solution Program

class BoardGame:
    def __init__(self):
        self.players = {}
        self.load_players()

    def load_players(self):
        """Load players from the `players.txt` file."""
        try:
            with open('players.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split(',')
                    self.players[name] = int(score)
        except FileNotFoundError:
            # No action needed if the file doesn't exist yet
            pass

    def save_players(self):
        """Save players to the `players.txt` file."""
        with open('players.txt', 'w') as file:
            for name, score in self.players.items():
                file.write(f'{name},{score}\n')

    def add_player(self, name, initial_score):
        """Add a new player with the specified name and initial score."""
        if name not in self.players:
            self.players[name] = initial_score
            self.save_players()

    def update_score(self, name, points):
        """Update score of the specified player by adding the given points."""
        if name in self.players:
            self.players[name] += points
            self.save_players()

    def get_highest_score(self):
        """Return the name of the player with the highest score."""
        if not self.players:
            return None
        highest_scorer = None
        highest_score = -float('inf')
        for name, score in self.players.items():
            if score > highest_score:
                highest_score = score
                highest_scorer = name
            elif score == highest_score and highest_scorer is None:
                highest_scorer = name
        return highest_scorer