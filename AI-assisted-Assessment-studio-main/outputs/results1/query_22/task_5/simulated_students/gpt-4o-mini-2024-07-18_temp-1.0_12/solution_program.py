def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = file.readlines()

    winner = None
    highest_average_score = -1

    for player in players:
        name, score, rounds = player.strip().split(':')
        score = int(score)
        rounds = int(rounds)
        average_score = score / rounds

        if (average_score > highest_average_score) or (average_score == highest_average_score and (winner is None or rounds < int(winner[1]))):
            winner = (name, rounds)
            highest_average_score = average_score

    return winner[0]