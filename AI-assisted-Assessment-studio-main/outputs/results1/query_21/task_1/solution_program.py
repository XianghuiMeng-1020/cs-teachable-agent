class GameBoard:
    def __init__(self, input_file):
        self.scores = {}
        with open(input_file, 'r') as file:
            for line in file:
                player_name = line.strip()
                self.scores[player_name] = 0

    def add_round_scores(self, player_name, round1_score, round2_score):
        if player_name in self.scores:
            total_round_score = round1_score + round2_score
            self.scores[player_name] += total_round_score

    def get_total_score(self, player_name):
        return self.scores.get(player_name, 0)

    def get_winner(self):
        if not self.scores:
            return None
        max_score = max(self.scores.values())
        for player_name, score in self.scores.items():
            if score == max_score:
                return player_name

    def write_scores_to_file(self, output_file):
        with open(output_file, 'w') as file:
            for player_name, score in self.scores.items():
                file.write(f"{player_name}: {score}\n")
