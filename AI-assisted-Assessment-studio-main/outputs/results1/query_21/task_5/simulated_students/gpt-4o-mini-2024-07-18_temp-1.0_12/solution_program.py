class BoardGameLeaderboard:
    def __init__(self):
        self.scores = {}
        self.load_from_file()

    def add_score(self, player_name, score):
        if player_name in self.scores:
            self.scores[player_name] += score
        else:
            self.scores[player_name] = score
        self.save_to_file()

    def get_score(self, player_name):
        return self.scores.get(player_name, 0)

    def get_top_player(self):
        if not self.scores:
            return None
        return max(self.scores, key=self.scores.get)

    def load_from_file(self):
        try:
            with open('leaderboard.txt', 'r') as file:
                for line in file:
                    if line.strip():
                        player_name, score = line.strip().split(':')
                        self.scores[player_name] = int(score)
        except FileNotFoundError:
            pass

    def save_to_file(self):
        with open('leaderboard.txt', 'w') as file:
            for player_name, score in self.scores.items():
                file.write(f'{player_name}:{score}\n')