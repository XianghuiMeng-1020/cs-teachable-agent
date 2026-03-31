def calculate_final_score(moves):
    rolls = moves.split(',')
    position = 0
    for roll in rolls:
        try:
            dice_roll = int(roll)
            if 1 <= dice_roll <= 6:
                if position + dice_roll <= 100:
                    position += dice_roll
        except ValueError:
            continue
    return position