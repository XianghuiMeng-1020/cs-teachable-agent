def calculate_final_score(moves):
    rolls = moves.split(',')
    score = 0
    for roll in rolls:
        if roll.isdigit():
            die_roll = int(roll)
            if 1 <= die_roll <= 6:
                if score + die_roll <= 100:
                    score += die_roll
    return score