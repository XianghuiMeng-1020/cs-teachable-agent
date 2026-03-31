def play_dice_game(target):
    rolls = 0
    score = 0
    while score < target:
        rolls += 1
        score += 6  # to maximize the score in each roll
    return rolls