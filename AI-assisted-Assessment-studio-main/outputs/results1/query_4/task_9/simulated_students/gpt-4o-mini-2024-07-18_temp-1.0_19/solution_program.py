import random

def game_of_chance(player_score):
    player_name = list(player_score.keys())[0]
    player_wins = 0
    computer_wins = 0
    player_total = 0
    computer_total = 0

    for _ in range(5):
        player_total += random.randint(1, 6)
        computer_total += random.randint(1, 6)

    if player_total > computer_total:
        player_wins += 1
        player_score[player_name] += 1
    elif computer_total > player_total:
        computer_wins += 1
        if 'Computer' in player_score:
            player_score['Computer'] += 1
        else:
            player_score['Computer'] = 1

    return player_score