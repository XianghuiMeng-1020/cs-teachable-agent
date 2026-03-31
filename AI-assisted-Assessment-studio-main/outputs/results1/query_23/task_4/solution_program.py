class BoardGame:
    games = []

    def __init__(self, title, min_players, max_players):
        self.title = title
        self.min_players = min_players
        self.max_players = max_players

    @classmethod
    def add_game(cls, title, min_players, max_players):
        cls.games.append(BoardGame(title, min_players, max_players))

    @classmethod
    def games_with_min_players(cls, num):
        return [game.title for game in cls.games if game.min_players <= num]

    @classmethod
    def games_with_max_players(cls, num):
        return [game.title for game in cls.games if game.max_players >= num]