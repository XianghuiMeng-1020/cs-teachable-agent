import os

class BoardGameScoreboard:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                pass

    def add_score(self, player_name, score):
        scores = self.load_scores()
        if player_name in scores:
            scores[player_name] += score
        else:
            scores[player_name] = score
        self.save_scores(scores)

    def get_score(self, player_name):
        scores = self.load_scores()
        return scores.get(player_name, 0)

    def save_scores(self, scores):
        with open(self.filename, 'w') as f:
            for player, score in scores.items():
                f.write(f'{player}:{score}\n')

    def load_scores(self):
        scores = {}
        with open(self.filename, 'r') as f:
            for line in f:
                if line.strip():
                    player, score = line.strip().split(':')
                    scores[player] = int(score)
        return scores
