def calculate_scores(filename):
    players_wins = {}
    with open(filename, 'r') as file:
        for line in file:
            player1, player2, result = line.strip().split()
            if result == 'win':
                if player1 in players_wins:
                    players_wins[player1] += 1
                else:
                    players_wins[player1] = 1
                if player2 not in players_wins:
                    players_wins[player2] = 0
            else:
                if player2 in players_wins:
                    players_wins[player2] += 1
                else:
                    players_wins[player2] = 1
                if player1 not in players_wins:
                    players_wins[player1] = 0
    result_list = [(player, wins) for player, wins in players_wins.items() if wins > 0]
    return sorted(result_list, key=lambda x: (-x[1], x[0]))