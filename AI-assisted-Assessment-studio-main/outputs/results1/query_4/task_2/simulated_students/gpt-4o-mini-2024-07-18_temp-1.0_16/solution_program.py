def play_dice_game(target):
    rolls = 0
    current_score = 0
    while current_score < target:
        rolls += 1
        current_score += 6  # In the worst case, we consider the maximum roll of the die
    return rolls