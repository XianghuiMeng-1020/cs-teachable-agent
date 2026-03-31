class BoardGame:
    def __init__(self, name, players, status):
        self.name = name.lower()  # Ensure game name is lowercase
        self.players = [player.lower() for player in players]  # Ensure all player names are lowercase
        self.status = status.lower()  # Ensure status is lowercase

    def add_player(self, player_name):
        player_name = player_name.lower()
        if self.status == 'ongoing' and player_name not in self.players:
            self.players.append(player_name)

    def remove_player(self, player_name):
        player_name = player_name.lower()
        if player_name in self.players:
            self.players.remove(player_name)

    def finish_game(self):
        self.status = 'completed'

    def game_summary(self):
        return (f"Game: {self.name}, Players: {len(self.players)}, List: "
                f"[{', '.join(self.players)}], Status: {self.status}")

# Example usage
# bg = BoardGame("Catan", ["alice", "bob"], "ongoing")
# bg.add_player("charlie")
# bg.remove_player("alice")
# print(bg.game_summary())
# bg.finish_game()
# print(bg.game_summary())
