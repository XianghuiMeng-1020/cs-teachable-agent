class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def add_score(self, points):
        self.score += points

    def get_details(self):
        return f"Name: {self.name}, Score: {self.score}"


def read_players_from_file(filename):
    players = []
    with open(filename, 'r') as file:
        for line in file:
            name, score = line.strip().split(',')
            player = Player(name, int(score) + 2)
            players.append(player)
    return players