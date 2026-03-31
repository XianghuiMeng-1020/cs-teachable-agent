def play_dice_game(target):
    rolls = 0
    score = 0
    while score < target:
        rolls += 1
        score += 6  # Assuming the best case, where each roll is 6
    return rolls