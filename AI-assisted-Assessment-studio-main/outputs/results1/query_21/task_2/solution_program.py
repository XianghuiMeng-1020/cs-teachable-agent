class Game:
    def __init__(self, title, author, year, availability=True):
        self.title = title
        self.author = author
        self.year = year
        self.availability = availability

class Library:
    def __init__(self):
        self.collection = []

    def add_game(self, title, author, year):
        game = Game(title, author, year)
        self.collection.append(game)

    def borrow_game(self, title):
        for game in self.collection:
            if game.title == title and game.availability:
                game.availability = False
                return True
        return False

    def return_game(self, title):
        for game in self.collection:
            if game.title == title:
                game.availability = True

    def load_games(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            title, author, year, availability = line.strip().split(',')
            self.collection.append(Game(title, author, int(year), bool(int(availability))))

    def save_games(self, file_path):
        with open(file_path, 'w') as file:
            for game in self.collection:
                file.write(f"{game.title},{game.author},{game.year},{int(game.availability)}\n")
