class BoardGame:
    def __init__(self):
        self.players = []

    def add_player(self, player_name):
        # Convert player name to lowercase for case-insensitivity
        player_name_lower = player_name.lower()
        # Check for unique addition to list
        if player_name_lower not in [player.lower() for player in self.players]:
            self.players.append(player_name)

    def remove_player(self, player_name):
        # Convert player name to lowercase for case-insensitivity
        player_name_lower = player_name.lower()
        # Attempt to remove the player if they exist in the list
        for player in self.players:
            if player.lower() == player_name_lower:
                self.players.remove(player)
                break

    def get_players(self):
        # Return list of players as a comma-separated string or indicate no players
        if self.players:
            return ", ".join(self.players)
        else:
            return "No players"
