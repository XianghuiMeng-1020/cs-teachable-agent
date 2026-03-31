def lucky_dice(outcomes):
    total_score = 0
    scores = []
    for roll in outcomes:
        dice_sum = sum(roll)
        if dice_sum in {7, 11}:
            score = 10
        elif dice_sum in {2, 3, 12}:
            score = 5
        else:
            score = 0
        scores.append(score)
        total_score += score
    return {'total_score': total_score, 'rolls': scores}