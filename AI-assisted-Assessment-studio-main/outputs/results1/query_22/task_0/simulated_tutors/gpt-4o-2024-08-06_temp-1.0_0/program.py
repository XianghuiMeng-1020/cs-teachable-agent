def calculate_scores(filename):
    player_wins = {}

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                player1, player2, result = parts
                if result == "win":
                    if player1 in player_wins:
                        player_wins[player1] += 1
                    else:
                        player_wins[player1] = 1
                elif result == "lose":
                    if player2 in player_wins:
                        player_wins[player2] += 1
                    else:
                        player_wins[player2] = 1

    # Create list of players with at least one win
    winners = [(player, wins) for player, wins in player_wins.items() if wins > 0]
    # Sort by number of wins (descending), then by player name (ascending)
    winners.sort(key=lambda x: (-x[1], x[0]))

    return winners