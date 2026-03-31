def play_dice_game(target):
    rolls = 0
    current_score = 0
    while current_score < target:
        rolls += 1
        current_score += 6  # Maximum score that can be achieved with one roll
    return rolls