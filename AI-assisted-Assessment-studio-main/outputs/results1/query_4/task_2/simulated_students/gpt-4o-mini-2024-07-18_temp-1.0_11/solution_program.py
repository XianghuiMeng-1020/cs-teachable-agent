def play_dice_game(target):
    rolls = 0
    score = 0
    while score < target:
        rolls += 1
        score += 6  # Maximum score from a single die roll
    return rolls