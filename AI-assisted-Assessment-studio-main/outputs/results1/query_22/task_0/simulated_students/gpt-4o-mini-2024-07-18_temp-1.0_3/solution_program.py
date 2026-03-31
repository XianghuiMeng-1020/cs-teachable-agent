def calculate_scores(filename):
    scores = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            player1 = parts[0]
            player2 = parts[1]
            result = parts[2]
            if result == 'win':
                scores[player1] = scores.get(player1, 0) + 1
                scores[player2] = scores.get(player2, 0)
            elif result == 'lose':
                scores[player2] = scores.get(player2, 0) + 1
                scores[player1] = scores.get(player1, 0)
    result = [(player, count) for player, count in scores.items() if count > 0]
    result.sort(key=lambda x: (-x[1], x[0]))
    return result