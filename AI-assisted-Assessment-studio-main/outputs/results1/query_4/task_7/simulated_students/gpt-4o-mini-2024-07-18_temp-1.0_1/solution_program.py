def dice_probability(target_score):
    if target_score < 2 or target_score > 12:
        return 0.0

    favorable_outcomes = 0
    total_outcomes = 36  # 6 sides on the first die * 6 sides on the second die

    for die1 in range(1, 7):
        for die2 in range(1, 7):
            if die1 + die2 == target_score:
                favorable_outcomes += 1

    probability = favorable_outcomes / total_outcomes
    return round(probability, 4)