class GameBoard:
    def __init__(self, input_file):
        self.players_scores = {}
        self.load_players(input_file)

    def load_players(self, input_file):
        with open(input_file, 'r') as file:
            for line in file:
                player_name = line.strip()
                if player_name:
                    self.players_scores[player_name] = 0

    def add_round_scores(self, player_name, round1_score, round2_score):
        if player_name in self.players_scores:
            self.players_scores[player_name] += round1_score + round2_score

    def get_total_score(self, player_name):
        return self.players_scores.get(player_name, 0)

    def get_winner(self):
        return max(self.players_scores, key=self.players_scores.get)

    def write_scores_to_file(self, output_file):
        with open(output_file, 'w') as file:
            for player_name, total_score in self.players_scores.items():
                file.write(f"{player_name}: {total_score}\n")