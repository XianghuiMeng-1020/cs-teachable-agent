class BoardGame:
    def __init__(self, name, num_players, play_time):
        self.name = name
        self.num_players = num_players
        self.play_time = play_time

    def to_string(self):
        return f"{self.name},{self.num_players},{self.play_time}"


class BoardGameCollection:
    def __init__(self, games=None):
        if games is None:
            games = []
        self.games = []
        for game in games:
            self.add_game(game)

    def add_game(self, game):
        if not any(existing_game.name == game.name for existing_game in self.games):
            self.games.append(game)

    def to_file(self, filename):
        with open(filename, 'w') as file:
            for game in self.games:
                file.write(game.to_string() + '\n')

    def from_file(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                name, num_players, play_time = line.strip().split(',')
                game = BoardGame(name, int(num_players), int(play_time))
                self.add_game(game)