import random

def game_of_chance(player_score):
    player_name = list(player_score.keys())[0]
    player_total = 0
    computer_total = 0

    for _ in range(5):
        player_roll = random.randint(1, 6)
        computer_roll = random.randint(1, 6)
        player_total += player_roll
        computer_total += computer_roll

    if player_total > computer_total:
        player_score[player_name] += 1
    elif computer_total > player_total:
        player_score['Computer'] = player_score.get('Computer', 0) + 1

    return player_score