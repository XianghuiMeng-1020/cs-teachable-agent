class BoardGame:
    games = []

    @classmethod
    def add_game(cls, title, min_players, max_players):
        game = {'title': title, 'min_players': min_players, 'max_players': max_players}
        cls.games.append(game)

    @classmethod
    def games_with_min_players(cls, num):
        return [game['title'] for game in cls.games if game['min_players'] <= num]

    @classmethod
    def games_with_max_players(cls, num):
        return [game['title'] for game in cls.games if game['max_players'] >= num]