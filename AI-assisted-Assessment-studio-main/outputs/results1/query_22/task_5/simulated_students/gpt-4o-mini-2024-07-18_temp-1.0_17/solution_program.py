def calculate_winner_board_game(file_path):
    with open(file_path, 'r') as file:
        players = []
        for line in file:
            player_info = line.strip().split(':')
            player_name = player_info[0]
            score = int(player_info[1])
            rounds = int(player_info[2])
            average_score = score / rounds
            players.append((player_name, average_score, rounds))

    # Sort players first by average score (descending) and then by rounds (ascending)
    players.sort(key=lambda x: (-x[1], x[2]))

    return players[0][0]