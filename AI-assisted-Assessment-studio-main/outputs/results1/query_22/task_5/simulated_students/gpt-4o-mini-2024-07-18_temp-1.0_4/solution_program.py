def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = []
        for line in file:
            name, score_str, rounds_str = line.strip().split(':')
            score = int(score_str)
            rounds = int(rounds_str)
            average_score_per_round = score / rounds
            players.append((name, average_score_per_round, rounds))

    players.sort(key=lambda x: (-x[1], x[2]))
    return players[0][0]