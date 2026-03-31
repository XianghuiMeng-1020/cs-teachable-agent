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
    scores = data.split(',')
    player_dict = {}

    for score_entry in scores:
        name, score = score_entry.split(':')
        score = int(score)
        if name not in player_dict:
            player_dict[name] = PlayerScore(name)
        player_dict[name].add_score(score)

    return list(player_dict.values())