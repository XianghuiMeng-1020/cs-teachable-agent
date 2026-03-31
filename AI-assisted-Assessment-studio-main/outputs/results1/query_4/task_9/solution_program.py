import random

def game_of_chance(player_score):
    player_total = 0
    computer_total = 0
    for _ in range(5):
        player_total += random.randint(1, 6)
        computer_total += random.randint(1, 6)
        
    if player_total > computer_total:
        for player in player_score:
            player_score[player] += 1
        
    elif computer_total > player_total:
        if 'Computer' not in player_score:
            player_score['Computer'] = 0
        player_score['Computer'] += 1
    return player_score

# Set seed for consistent testing; however, during real usage, random.seed should not be called.
random.seed(42)