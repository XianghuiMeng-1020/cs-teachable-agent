class GameBoard:
    def __init__(self, input_file):
        self.players = {}
        with open(input_file, 'r') as file:
            for line in file:
                player_name = line.strip()
                self.players[player_name] = 0

    def add_round_scores(self, player_name, round1_score, round2_score):
        if player_name in self.players:
            self.players[player_name] += round1_score + round2_score

    def get_total_score(self, player_name):
        return self.players.get(player_name, 0)

    def get_winner(self):
        if not self.players:
            return None
        max_score = max(self.players.values())
        for player, score in self.players.items():
            if score == max_score:
                return player

    def write_scores_to_file(self, output_file):
        with open(output_file, 'w') as file:
            for player, score in self.players.items():
                file.write(f'{player}: {score}\n')