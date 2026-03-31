def calculate_scores(filename):
    scores = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('
')
            for game in parts:
                player1, player2, result = game.split()
                if result == 'win':
                    scores[player1] = scores.get(player1, 0) + 1
                    scores[player2] = scores.get(player2, 0)
                elif result == 'lose':
                    scores[player2] = scores.get(player2, 0) + 1
                    scores[player1] = scores.get(player1, 0)
    winners = [(player, count) for player, count in scores.items() if count > 0]
    winners.sort(key=lambda x: (-x[1], x[0]))
    return winners
