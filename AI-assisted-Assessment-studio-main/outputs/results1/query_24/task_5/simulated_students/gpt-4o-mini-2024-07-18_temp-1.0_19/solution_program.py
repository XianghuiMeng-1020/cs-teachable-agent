def calculate_final_score(moves):
    position = 0
    rolls = moves.split(',')
    for roll in rolls:
        try:
            value = int(roll)
            if 1 <= value <= 6:
                if position + value <= 100:
                    position += value
        except ValueError:
            continue
    return position