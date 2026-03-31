class GameBoard:
    def __init__(self, input_file):
        self.players = {}
        self.load_players(input_file)

    def load_players(self, input_file):
        with open(input_file, 'r') as file:
            for line in file:
                player_name = line.strip()
                self.players[player_name] = 0

    def add_round_scores(self, player_name, round1_score, round2_score):
        if player_name in self.players:
            self.players[player_name] += round1_score + round2_score

    def get_total_score(self, player_name):
        if player_name in self.players:
            return self.players[player_name]
        return None

    def get_winner(self):
        if not self.players:
            return None
        winner = max(self.players, key=self.players.get)
        return winner

    def write_scores_to_file(self, output_file):
        with open(output_file, 'w') as file:
            for player_name, total_score in self.players.items():
                file.write(f'{player_name}: {total_score}\n')