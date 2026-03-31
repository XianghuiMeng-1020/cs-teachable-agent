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
                scores[player1] += 1
                if player2 not in scores:
                    scores[player2] = 0
            else:  # player1 loses
                if player2 not in scores:
                    scores[player2] = 0
                scores[player2] += 1
                if player1 not in scores:
                    scores[player1] = 0

    sorted_scores = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return [(player, score) for player, score in sorted_scores if score > 0]