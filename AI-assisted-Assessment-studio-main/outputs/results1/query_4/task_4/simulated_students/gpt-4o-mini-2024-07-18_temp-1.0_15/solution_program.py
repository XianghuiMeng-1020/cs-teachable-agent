import random

def lucky_number_game():
    score_mapping = {1: 0, 2: 10, 3: -5, 4: 5, 5: 20, 6: -10}
    total_score = 0
    rolls = 0
    
    while total_score <= 0:
        roll = random.randint(1, 6)
        total_score += score_mapping[roll]
        rolls += 1
    
    return rolls