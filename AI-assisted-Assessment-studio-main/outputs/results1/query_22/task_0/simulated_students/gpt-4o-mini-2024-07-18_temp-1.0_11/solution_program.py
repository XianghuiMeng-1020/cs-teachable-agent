def calculate_scores(filename):
    from collections import defaultdict

    scores = defaultdict(int)

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            player1, player2, result = parts[0], parts[1], parts[2]
            if result == 'win':
                scores[player1] += 1
            else:
                scores[player2] += 1

    sorted_scores = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    return [player for player in sorted_scores if player[1] > 0]