class BoardGame:
    def __init__(self, name, min_players, max_players):
        self.name = name
        self.min_players = min_players
        self.max_players = max_players

    def __str__(self):
        return f"{self.name} ({self.min_players}:{self.max_players} players)"


def save_board_games(board_games):
    with open('board_games.txt', 'w') as f:
        for game in board_games:
            f.write(f"{game.name},{game.min_players},{game.max_players}\n")


def load_board_games():
    board_games = []
    try:
        with open('board_games.txt', 'r') as f:
            lines = f.readlines()
        for line in lines:
            name, min_players, max_players = line.strip().split(',')
            board_games.append(BoardGame(name, int(min_players), int(max_players)))
    except FileNotFoundError:
        pass
    return board_games