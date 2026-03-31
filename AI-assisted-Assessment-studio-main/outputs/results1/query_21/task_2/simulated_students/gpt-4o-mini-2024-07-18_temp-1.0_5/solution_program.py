class Game:
    def __init__(self, title, author, year, availability=True):
        self.title = title
        self.author = author
        self.year = year
        self.availability = availability

class Library:
    def __init__(self):
        self.games = []

    def add_game(self, title, author, year):
        game = Game(title, author, year)
        self.games.append(game)

    def borrow_game(self, title):
        for game in self.games:
            if game.title == title and game.availability:
                game.availability = False
                return True
        return False

    def return_game(self, title):
        for game in self.games:
            if game.title == title:
                game.availability = True
                return

    def load_games(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                title, author, year, availability = line.strip().split(',')
                game = Game(title, author, int(year), availability == '1')
                self.games.append(game)

    def save_games(self, file_path):
        with open(file_path, 'w') as file:
            for game in self.games:
                availability = '1' if game.availability else '0'
                file.write(f'{game.title},{game.author},{game.year},{availability}\n')