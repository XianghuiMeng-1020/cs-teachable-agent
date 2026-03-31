def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    winner = None
    best_average = 0
    best_rounds = float('inf')

    for player in players:
        name, score, rounds = player.strip().split(':')
        score = int(score)
        rounds = int(rounds)
        average_score_per_round = score / rounds

        if (average_score_per_round > best_average) or (
            average_score_per_round == best_average and rounds < best_rounds):
            winner = name
            best_average = average_score_per_round
            best_rounds = rounds

    return winner