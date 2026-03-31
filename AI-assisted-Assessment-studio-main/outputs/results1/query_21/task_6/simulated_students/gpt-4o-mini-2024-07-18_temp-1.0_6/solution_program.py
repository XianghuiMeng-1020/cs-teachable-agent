class BoardGameScoreboard:
    def __init__(self, filename):
        self.filename = filename
        self.scoreboard = {}
        self.load_scores()

    def load_scores(self):
        try:
            with open(self.filename, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    player, score = line.strip().split(':')
                    self.scoreboard[player] = int(score)
        except FileNotFoundError:
            pass

    def save_scores(self):
        with open(self.filename, 'w') as file:
            for player, score in self.scoreboard.items():
                file.write(f'{player}:{score}\n')

    def add_score(self, player_name, score):
        if player_name in self.scoreboard:
            self.scoreboard[player_name] += score
        else:
            self.scoreboard[player_name] = score
        self.save_scores()

    def get_score(self, player_name):
        return self.scoreboard.get(player_name, 0)