def calculate_final_score(moves):
    moves_list = moves.split(',')
    position = 0
    for move in moves_list:
        try:
            roll = int(move)
            if 1 <= roll <= 6:
                if position + roll <= 100:
                    position += roll
        except ValueError:
            continue
    return position