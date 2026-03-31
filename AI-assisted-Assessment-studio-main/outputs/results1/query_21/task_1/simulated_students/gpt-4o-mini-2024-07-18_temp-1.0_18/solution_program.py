class GameBoard:
    def __init__(self, input_file):
        self.scores = {}
        self.load_players(input_file)

    def load_players(self, input_file):
        with open(input_file, 'r') as file:
            players = file.readlines()
            for player in players:
                self.scores[player.strip()] = 0

    def add_round_scores(self, player_name, round1_score, round2_score):
        if player_name in self.scores:
            self.scores[player_name] += round1_score + round2_score

    def get_total_score(self, player_name):
        return self.scores.get(player_name, None)

    def get_winner(self):
        winner = max(self.scores, key=self.scores.get)
        return winner

    def write_scores_to_file(self, output_file):
        with open(output_file, 'w') as file:
            for player, score in self.scores.items():
                file.write(f'{player}: {score}\n')