def calculate_final_score(moves):
    position = 0
    rolls = moves.split(',')
    
    for roll in rolls:
        try:
            roll_value = int(roll)
            if 1 <= roll_value <= 6:
                if position + roll_value <= 100:
                    position += roll_value
        except ValueError:
            continue
    
    return position