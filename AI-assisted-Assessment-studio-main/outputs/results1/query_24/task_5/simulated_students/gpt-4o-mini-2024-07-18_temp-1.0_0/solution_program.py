def calculate_final_score(moves):
    rolls = moves.split(',')
    position = 0
    for roll in rolls:
        try:
            move = int(roll)
            if 1 <= move <= 6:
                if position + move <= 100:
                    position += move
        except ValueError:
            continue
    return position