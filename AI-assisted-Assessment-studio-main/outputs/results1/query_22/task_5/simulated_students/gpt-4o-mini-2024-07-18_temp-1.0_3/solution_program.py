def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    max_average = -1
    winner = None

    for player in players:
        name, score, rounds = player.strip().split(':')
        score = int(score)
        rounds = int(rounds)
        average_score = score / rounds

        if (average_score > max_average) or (
            average_score == max_average and rounds < (int(winner.split(':')[2]) if winner else float('inf')))
        ): 
            max_average = average_score
            winner = f'{name}:{score}:{rounds}'

    return winner.split(':')[0]