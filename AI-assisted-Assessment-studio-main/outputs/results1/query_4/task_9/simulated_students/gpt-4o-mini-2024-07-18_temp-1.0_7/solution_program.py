import random

def game_of_chance(player_score):
    player_rolls = sum(random.randint(1, 6) for _ in range(5))
    computer_rolls = sum(random.randint(1, 6) for _ in range(5))

    if player_rolls > computer_rolls:
        player_score[list(player_score.keys())[0]] += 1
    elif computer_rolls > player_rolls:
        if 'Computer' in player_score:
            player_score['Computer'] += 1
        else:
            player_score['Computer'] = 1

    return player_score