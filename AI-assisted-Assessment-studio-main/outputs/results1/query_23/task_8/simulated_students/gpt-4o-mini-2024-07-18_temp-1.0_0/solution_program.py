class PlayerScore:
    def __init__(self, name):
        self.name = name
        self.highest_score = 0

    def add_score(self, score):
        if score > self.highest_score:
            self.highest_score = score

    def get_score(self):
        return self.highest_score

    def __str__(self):
        return f'Player: {self.name}, Highest Score: {self.highest_score}'


def parse_scores(data):
    players = {}
    entries = data.split(',')
    for entry in entries:
        name, score = entry.split(':')
        score = int(score)
        if name not in players:
            players[name] = PlayerScore(name)
        players[name].add_score(score)
    return list(players.values())