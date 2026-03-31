def play_dice_game(target):
    # Each roll at maximum can add 6 to the score.
    # To determine the minimal number of rolls, we can
    # use the formula: rolls = ceil(target / 6)
    import math
    rolls = math.ceil(target / 6)
    return rolls