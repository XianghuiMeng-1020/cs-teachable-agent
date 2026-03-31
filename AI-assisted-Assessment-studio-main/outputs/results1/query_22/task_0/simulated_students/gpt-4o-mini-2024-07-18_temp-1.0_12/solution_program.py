def calculate_scores(filename):
    scores = {}

    with open(filename, 'r') as file:
        for line in file:
            player1, player2, result = line.split()  # unpack line content
            if result == 'win':
                scores[player1] = scores.get(player1, 0) + 1  # Increment player1's score
                scores[player2] = scores.get(player2, 0)  # Ensure player2 exists in scores
            elif result == 'lose':
                scores[player2] = scores.get(player2, 0) + 1  # Increment player2's score
                scores[player1] = scores.get(player1, 0)  # Ensure player1 exists in scores

    # Filter out players with zero wins and sort by wins and name
    ranked_players = sorted((player, win) for player, win in scores.items() if win > 0)
    ranked_players.sort(key=lambda x: (-x[1], x[0]))  # Sort by descending wins and then by name

    return ranked_players