def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    winner = None
    highest_average_score = -1

    for line in lines:
        parts = line.strip().split(':')
        player_name = parts[0]
        score = int(parts[1])
        rounds = int(parts[2])

        average_score = score / rounds

        if (average_score > highest_average_score or
            (average_score == highest_average_score and rounds < (lines[winner][2] if winner is not None else float('inf'))))):
            winner = player_name
            highest_average_score = average_score

    return winner