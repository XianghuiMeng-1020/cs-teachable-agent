def calculate_scores(filename):
    scores = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            player1, player2, result = parts[0], parts[1], parts[2]
            if result == 'win':
                if player1 not in scores:
                    scores[player1] = 0
                scores[player1] += 1
                if player2 not in scores:
                    scores[player2] = 0
            elif result == 'lose':
                if player2 not in scores:
                    scores[player2] = 0
                scores[player2] += 1
                if player1 not in scores:
                    scores[player1] = 0

    sorted_scores = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return [(player, win) for player, win in sorted_scores if win > 0]