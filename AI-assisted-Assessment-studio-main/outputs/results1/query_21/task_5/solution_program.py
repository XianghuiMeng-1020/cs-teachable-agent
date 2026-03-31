class BoardGameLeaderboard:
    def __init__(self):
        self.scores = {}

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
        return max(self.scores, key=self.scores.get)

    def load_from_file(self):
        self.scores.clear()
        try:
            with open('leaderboard.txt', 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        name, score = line.split(':')
                        self.scores[name] = int(score)
        except FileNotFoundError:
            pass
        
    def save_to_file(self):
        with open('leaderboard.txt', 'w') as f:
            for name, score in self.scores.items():
                f.write(f"{name}:{score}\n")
