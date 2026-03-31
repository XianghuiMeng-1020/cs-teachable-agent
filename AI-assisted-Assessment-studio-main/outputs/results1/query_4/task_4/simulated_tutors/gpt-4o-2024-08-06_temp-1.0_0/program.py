import random

def lucky_number_game() -> int:
    score_map = {
        1: 0,
        2: 10,
        3: -5,
        4: 5,
        5: 20,
        6: -10
    }
    score = 0
    rolls = 0
    
    # Roll the dice until we reach a positive net gain
    while score <= 0:
        dice_roll = random.randint(1, 6)
        score += score_map[dice_roll]
        rolls += 1
    
    return rolls
