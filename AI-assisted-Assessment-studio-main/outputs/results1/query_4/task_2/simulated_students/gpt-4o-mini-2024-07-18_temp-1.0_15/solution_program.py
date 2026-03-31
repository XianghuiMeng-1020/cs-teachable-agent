def play_dice_game(target):
    # The maximum score from one roll is 6
    max_roll = 6
    # Calculate the minimum number of rolls needed using ceiling division
    rolls_needed = -(-target // max_roll)
    return rolls_needed