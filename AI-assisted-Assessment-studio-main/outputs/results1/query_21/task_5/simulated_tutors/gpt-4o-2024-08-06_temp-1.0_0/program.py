class BoardGameLeaderboard:
    def __init__(self):
        self.scores = {}

    def load_from_file(self):
        try:
            with open('leaderboard.txt', 'r') as file:
                for line in file:
                    name, score = line.strip().split(':')
                    self.scores[name] = int(score)
        except FileNotFoundError:
            # If the file does not exist, start with an empty leaderboard
            self.scores = {}

    def save_to_file(self):
        with open('leaderboard.txt', 'w') as file:
            for player, score in self.scores.items():
                file.write(f'{player}:{score}\n')

    def add_score(self, player_name, score):
        if player_name in self.scores:
            self.scores[player_name] += score
        else:
            self.scores[player_name] = score

    def get_score(self, player_name):
        return self.scores.get(player_name, 0)

    def get_top_player(self):
        if not self.scores:
            return None
        top_player = max(self.scores, key=self.scores.get)
        return top_player