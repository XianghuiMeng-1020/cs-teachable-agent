class GameBoard:
    def __init__(self, filename):
        self.players = {}
        # Read player names from a file
        with open(filename, 'r') as file:
            for line in file:
                player_name = line.strip()
                self.players[player_name] = 0

    def add_round_scores(self, player_name, round1_score, round2_score):
        if player_name in self.players:
            # Add the sum of scores from both rounds to the player's total score
            self.players[player_name] += round1_score + round2_score

    def get_total_score(self, player_name):
        # Return the player's total score or 0 if they don't exist
        return self.players.get(player_name, 0)

    def get_winner(self):
        if not self.players:
            return None
        return max(self.players, key=self.players.get)

    def write_scores_to_file(self, output_file):
        with open(output_file, 'w') as file:
            for player, score in self.players.items():
                file.write(f"{player}: {score}\n")
