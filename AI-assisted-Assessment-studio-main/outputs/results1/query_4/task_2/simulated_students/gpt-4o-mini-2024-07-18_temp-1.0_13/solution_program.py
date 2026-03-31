def play_dice_game(target):
    rolls = 0
    score = 0
    while score < target:
        score += 6  # Assume the best possible roll is always 6
        rolls += 1
    return rolls