def lucky_dice(outcomes):
    total_score = 0
    rolls = []
    for roll in outcomes:
        sum_roll = sum(roll)
        if sum_roll in (7, 11):
            score = 10
        elif sum_roll in (2, 3, 12):
            score = 5
        else:
            score = 0
        rolls.append(score)
        total_score += score
    return {'total_score': total_score, 'rolls': rolls}