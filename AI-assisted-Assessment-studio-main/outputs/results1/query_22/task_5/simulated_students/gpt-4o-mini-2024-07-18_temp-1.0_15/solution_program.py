def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    best_player = None
    best_average = -1
    best_rounds = float('inf')

    for player in players:
        name, score, rounds = player.strip().split(':')
        score = int(score)
        rounds = int(rounds)
        average_score = score / rounds

        if (average_score > best_average) or (average_score == best_average and rounds < best_rounds):
            best_player = name
            best_average = average_score
            best_rounds = rounds

    return best_player