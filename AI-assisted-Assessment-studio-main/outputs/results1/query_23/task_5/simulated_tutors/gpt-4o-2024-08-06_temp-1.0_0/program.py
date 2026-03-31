class ScoreCard:
    def __init__(self, players):
        # Initialize a dictionary to keep track of each player's score
        self.scores = {player: 0 for player in players}
        self.players = players  # Maintain the list of players

    def add_score(self, player, points):
        # Add points to the player's score if the player exists
        if player in self.scores:
            self.scores[player] += points

    def get_score(self, player):
        # Return the player's score or None if player not found
        return self.scores.get(player, None)

    def get_winner(self):
        # Find the player with the highest score
        max_score = max(self.scores.values())
        for player in self.players:
            if self.scores[player] == max_score:
                return player