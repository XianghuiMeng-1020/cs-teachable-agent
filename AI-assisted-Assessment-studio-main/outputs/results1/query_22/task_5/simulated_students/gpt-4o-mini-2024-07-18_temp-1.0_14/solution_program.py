def calculate_winner_board_game(file_path):
    players = {}
    with open(file_path, 'r') as file:
        for line in file:
            name, score, rounds = line.strip().split(':')
            score = int(score)
            rounds = int(rounds)
            average_score = score / rounds
            players[name] = (average_score, rounds)

    winner = None
    for player, (avg_score, rounds) in players.items():
        if winner is None:
            winner = (player, avg_score, rounds)
        else:
            winner_name, winner_avg, winner_rounds = winner
            if (avg_score > winner_avg) or (avg_score == winner_avg and rounds < winner_rounds):
                winner = (player, avg_score, rounds)

    return winner[0]