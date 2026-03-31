def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = {}
        for line in file:
            name, score, rounds = line.strip().split(':')
            score = int(score)
            rounds = int(rounds)
            average_score = score / rounds
            players[name] = (average_score, rounds)

    winner = None
    max_average = -1
    min_rounds = float('inf')

    for player, (average, rounds) in players.items():
        if (average > max_average) or (average == max_average and rounds < min_rounds):
            max_average = average
            min_rounds = rounds
            winner = player

    return winner