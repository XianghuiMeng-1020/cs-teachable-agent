def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    winner = None
    max_avg_score = -1
    min_rounds = float('inf')

    for player in players:
        name, score, rounds = player.strip().split(':')
        score = int(score)
        rounds = int(rounds)
        avg_score = score / rounds

        if (avg_score > max_avg_score) or (avg_score == max_avg_score and rounds < min_rounds):
            max_avg_score = avg_score
            min_rounds = rounds
            winner = name

    return winner