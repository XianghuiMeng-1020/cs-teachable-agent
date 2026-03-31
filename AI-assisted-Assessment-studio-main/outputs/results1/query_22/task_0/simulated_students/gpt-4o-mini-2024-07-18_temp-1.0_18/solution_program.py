def calculate_scores(filename):
    scores = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            player1, player2, result = parts[0], parts[1], parts[2]
            if result == 'win':
                scores[player1] = scores.get(player1, 0) + 1
                scores[player2] = scores.get(player2, 0)
            elif result == 'lose':
                scores[player2] = scores.get(player2, 0) + 1
                scores[player1] = scores.get(player1, 0)
    results = [(player, win_count) for player, win_count in scores.items() if win_count > 0]
    results.sort(key=lambda x: (-x[1], x[0]))
    return results