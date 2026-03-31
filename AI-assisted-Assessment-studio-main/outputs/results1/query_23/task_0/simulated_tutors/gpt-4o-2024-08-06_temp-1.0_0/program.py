class BoardGame:
    def __init__(self):
        self.players = {}

    def add_player(self, player_name):
        self.players[player_name] = []

    def record_score(self, player_name, score):
        if player_name in self.players:
            self.players[player_name].append(score)

    def get_player_total_score(self, player_name):
        if player_name in self.players:
            return sum(self.players[player_name])
        return 0

    def get_winner(self):
        highest_score = -1
        winner = None
        for player, scores in self.players.items():
            total_score = sum(scores)
            if total_score > highest_score or (total_score == highest_score and player < winner):
                highest_score = total_score
                winner = player
        return winner

# Test the BoardGame class
if __name__ == "__main__":
    game = BoardGame()
    game.add_player("Alice")
    game.add_player("Bob")
    game.record_score("Alice", 10)
    game.record_score("Alice", 20)
    game.record_score("Bob", 15)
    game.record_score("Bob", 25)
    print("Alice's total score:", game.get_player_total_score("Alice"))   # Output: 30
    print("Bob's total score:", game.get_player_total_score("Bob"))      # Output: 40
    print("Current winner:", game.get_winner())                         # Output: Bob