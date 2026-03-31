def calculate_scores(filename):
    scores = {}
    with open(filename, 'r') as file:
        for line in file:
            player1, player2, result = line.strip().split()
            if result == 'win':
                scores[player1] = scores.get(player1, 0) + 1
                scores[player2] = scores.get(player2, 0)
            elif result == 'lose':
                scores[player2] = scores.get(player2, 0) + 1
                scores[player1] = scores.get(player1, 0)
    return sorted(((player, wins) for player, wins in scores.items() if wins > 0), key=lambda x: (-x[1], x[0]))