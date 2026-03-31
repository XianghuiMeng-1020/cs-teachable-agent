def calculate_final_score(moves):
    moves_list = moves.split(',')
    position = 0

    for move in moves_list:
        try:
            move_int = int(move)
            if 1 <= move_int <= 6:
                if position + move_int <= 100:
                    position += move_int
        except ValueError:
            continue

    return position