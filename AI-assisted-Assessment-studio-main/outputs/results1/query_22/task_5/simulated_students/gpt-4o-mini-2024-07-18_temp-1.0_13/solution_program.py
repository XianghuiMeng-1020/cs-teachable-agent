def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    max_average_score = -1
    winner = None

    for player in players:
        name, score, rounds = player.strip().split(':')
        score = int(score)
        rounds = int(rounds)
        average_score = score / rounds

        if (average_score > max_average_score or
            (average_score == max_average_score and (winner_rounds := winner[1]) > rounds)):
            max_average_score = average_score
            winner = (name, rounds)

    return winner[0]