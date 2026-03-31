class GameBoard:
    def __init__(self, filename):
        self.scores = {}
        with open(filename, 'r') as file:
            for line in file:
                player = line.strip()
                self.scores[player] = 0

    def add_round_scores(self, player_name, round1_score, round2_score):
        if player_name in self.scores:
            self.scores[player_name] += round1_score + round2_score

    def get_total_score(self, player_name):
        return self.scores.get(player_name, 0)

    def get_winner(self):
        if not self.scores:
            return None
        return max(self.scores, key=self.scores.get)

    def write_scores_to_file(self, output_file):
        with open(output_file, 'w') as file:
            for player, score in self.scores.items():
                file.write(f'{player}: {score}\n')