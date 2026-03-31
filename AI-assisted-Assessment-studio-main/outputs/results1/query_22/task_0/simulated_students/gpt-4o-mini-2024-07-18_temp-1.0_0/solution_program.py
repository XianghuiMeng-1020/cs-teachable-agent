def calculate_scores(filename):
    scores = {}

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            player1 = parts[0]
            player2 = parts[1]
            result = parts[2]

            if player1 not in scores:
                scores[player1] = 0
            if player2 not in scores:
                scores[player2] = 0

            if result == 'win':
                scores[player1] += 1
            else:
                scores[player2] += 1

    sorted_scores = sorted(((player, wins) for player, wins in scores.items() if wins > 0), 
                           key=lambda x: (-x[1], x[0]))
    return sorted_scores