class BoardGameLeaderboard:
    def __init__(self, filename='leaderboard.txt'):
        self.leaderboard = {}
        self.filename = filename
        self.load_from_file()

    def add_score(self, player_name, score):
        if player_name in self.leaderboard:
            self.leaderboard[player_name] += score
        else:
            self.leaderboard[player_name] = score
        self.save_to_file()

    def get_score(self, player_name):
        return self.leaderboard.get(player_name, 0)

    def get_top_player(self):
        if not self.leaderboard:
            return None
        return max(self.leaderboard, key=self.leaderboard.get)

    def load_from_file(self):
        try:
            with open(self.filename, 'r') as file:
                for line in file:
                    player_name, score = line.strip().split(':')
                    self.leaderboard[player_name] = int(score)
        except FileNotFoundError:
            pass

    def save_to_file(self):
        with open(self.filename, 'w') as file:
            for player_name, score in self.leaderboard.items():
                file.write(f'{player_name}:{score}\n')