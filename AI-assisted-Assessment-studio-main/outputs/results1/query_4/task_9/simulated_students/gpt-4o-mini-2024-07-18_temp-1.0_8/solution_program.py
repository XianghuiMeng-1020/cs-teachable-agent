import random

def game_of_chance(player_score):
    player_score_current = 0
    computer_score_current = 0

    for _ in range(5):
        player_roll = random.randint(1, 6)
        computer_roll = random.randint(1, 6)
        player_score_current += player_roll
        computer_score_current += computer_roll

    if player_score_current > computer_score_current:
        player_name = next(iter(player_score))  # Take the first player's name
        player_score[player_name] += 1
    elif computer_score_current > player_score_current:
        if 'Computer' in player_score:
            player_score['Computer'] += 1
        else:
            player_score['Computer'] = 1

    return player_score