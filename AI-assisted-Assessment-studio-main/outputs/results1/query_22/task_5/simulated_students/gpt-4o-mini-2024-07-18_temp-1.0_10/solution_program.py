def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    winner = None
    highest_average = -1
    fewest_rounds = float('inf')

    for line in players:
        name, score, rounds = line.strip().split(':')
        score = int(score)
        rounds = int(rounds)

        average_score_per_round = score / rounds

        if (average_score_per_round > highest_average) or (
            average_score_per_round == highest_average and rounds < fewest_rounds):
            highest_average = average_score_per_round
            fewest_rounds = rounds
            winner = name

    return winner