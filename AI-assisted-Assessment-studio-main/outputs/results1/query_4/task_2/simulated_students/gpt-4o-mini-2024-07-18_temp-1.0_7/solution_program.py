def play_dice_game(target):
    # Each roll can give a maximum of 6 points
    # We need to find the minimum number of rolls to reach or exceed the target
    if target <= 0:
        return 0
    return (target + 5) // 6  # Utilizing integer division to calculate rolls needed.