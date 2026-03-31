def play_dice_game(target):
    # Each roll can add a maximum of 6
    max_roll_value = 6
    # Calculate the minimum number of rolls needed
    # Rolls needed will be the target divided by max roll value rounded up
    rolls_needed = (target + max_roll_value - 1) // max_roll_value
    return rolls_needed