import math

def play_dice_game(target):
    # The maximum roll from a six-sided die is 6.
    
    # We need to find minimum rolls where each roll could be maximum (6)
    # Calculate the number of rolls needed using ceil division
    rolls_needed = math.ceil(target / 6.0)
    return rolls_needed
