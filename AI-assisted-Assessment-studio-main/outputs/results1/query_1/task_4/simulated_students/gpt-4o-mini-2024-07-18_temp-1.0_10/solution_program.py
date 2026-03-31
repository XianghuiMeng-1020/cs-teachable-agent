def dice_game(num_rolls, dice_pairs):
    scores = []
    cumulative_score = 0
    for i in range(num_rolls):
        d1, d2 = dice_pairs[i]
        roll_sum = d1 + d2
        if roll_sum == 7 or roll_sum == 11:
            cumulative_score += 10
        elif roll_sum in [2, 3, 12]:
            cumulative_score -= 5
        scores.append(cumulative_score)
    return scores