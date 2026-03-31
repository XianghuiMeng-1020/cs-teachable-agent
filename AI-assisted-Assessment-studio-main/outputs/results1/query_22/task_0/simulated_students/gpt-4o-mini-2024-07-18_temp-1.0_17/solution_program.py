def calculate_scores(filename):
    scores = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            player1 = parts[0]
            player2 = parts[1]
            result = parts[2]

            if result == 'win':
                if player1 not in scores:
                    scores[player1] = 0
                if player2 not in scores:
                    scores[player2] = 0
                scores[player1] += 1
            else:
                if player1 not in scores:
                    scores[player1] = 0
                if player2 not in scores:
                    scores[player2] = 0
                scores[player2] += 1

    # Create a sorted list of players who have at least one win
    sorted_scores = sorted(((player, wins) for player, wins in scores.items() if wins > 0),
                           key=lambda x: (-x[1], x[0]))
    return sorted_scores