def dice_probability(target_score):
    if target_score < 2 or target_score > 12:
        return 0.0

    favorable_outcomes = 0
    total_outcomes = 36

    for a in range(1, 7):
        b = target_score - a
        if 1 <= b <= 6:
            favorable_outcomes += 1

    probability = favorable_outcomes / total_outcomes
    return round(probability, 4)