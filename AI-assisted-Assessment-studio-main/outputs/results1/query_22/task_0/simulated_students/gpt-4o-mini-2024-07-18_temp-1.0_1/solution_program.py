def calculate_scores(filename):
    with open(filename, 'r') as file:
        results = file.readlines()

    scores = {}

    for result in results:
        player1, player2, outcome = result.strip().split()
        if outcome == 'win':
            scores[player1] = scores.get(player1, 0) + 1
            scores[player2] = scores.get(player2, 0)
        elif outcome == 'lose':
            scores[player2] = scores.get(player2, 0) + 1
            scores[player1] = scores.get(player1, 0)

    sorted_scores = sorted(scores.items(), key=lambda item: (-item[1], item[0]))
    return [item for item in sorted_scores if item[1] > 0]