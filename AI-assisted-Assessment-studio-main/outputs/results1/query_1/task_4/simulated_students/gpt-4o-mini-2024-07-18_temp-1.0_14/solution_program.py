def dice_game(num_rolls, dice_pairs):
    cumulative_score = 0
    scores = []
    for i in range(num_rolls):
        d1, d2 = dice_pairs[i]
        roll_sum = d1 + d2
        if roll_sum in [7, 11]:
            cumulative_score += 10
        elif roll_sum in [2, 3, 12]:
            cumulative_score -= 5
        scores.append(cumulative_score)
    return scores