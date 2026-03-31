def calculate_final_score(moves):
    position = 0
    rolls = moves.split(',')
    for roll in rolls:
        try:
            die_value = int(roll)
            if 1 <= die_value <= 6:
                if position + die_value <= 100:
                    position += die_value
        except ValueError:
            continue
    return position