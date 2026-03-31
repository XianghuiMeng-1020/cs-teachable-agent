def calculate_final_score(moves):
    moves_list = moves.split(',')
    position = 0

    for roll in moves_list:
        try:
            roll=int(roll)
            if 1 <= roll <= 6:
                if position + roll <= 100:
                    position += roll
        except ValueError:
            continue

    return position