def lucky_dice(outcomes):
    total_score = 0
    rolls = []
    for outcome in outcomes:
        d1, d2 = outcome
        roll_sum = d1 + d2
        if roll_sum in [7, 11]:
            score = 10
        elif roll_sum in [2, 3, 12]:
            score = 5
        else:
            score = 0
        rolls.append(score)
        total_score += score
    return {'total_score': total_score, 'rolls': rolls}