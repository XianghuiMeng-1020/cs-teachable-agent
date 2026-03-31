def play_dice_game(target):
    rolls = 0
    score = 0
    # Since the maximum roll is 6, we need to determine the necessary number of rolls
    while score < target:
        rolls += 1
        score += 6  # Simulate the best possible outcome on a roll
    return rolls
