def calculate_final_score(moves):
    rolls = moves.split(',')
    position = 0
    for roll in rolls:
        try:
            roll = int(roll)
            if 1 <= roll <= 6:
                if position + roll <= 100:
                    position += roll
        except ValueError:
            continue
    return position