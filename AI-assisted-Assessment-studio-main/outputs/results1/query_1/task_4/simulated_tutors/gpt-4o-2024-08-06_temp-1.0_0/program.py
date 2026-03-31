def dice_game(num_rolls, dice_pairs):
    score = 0
    scores = []
    for i in range(num_rolls):
        d1, d2 = dice_pairs[i]
        roll_sum = d1 + d2
        if roll_sum in [7, 11]:
            score += 10
        elif roll_sum in [2, 3, 12]:
            score -= 5
        # No score change for other sums
        scores.append(score)
    return scores

# Example usage:
dice_pairs = [(1, 6), (6, 6), (1, 1), (6, 5)]
result = dice_game(4, dice_pairs)
print(result)  # Output should be [10, 5, 0, 10]