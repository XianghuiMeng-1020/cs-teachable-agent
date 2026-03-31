import random

def game_of_chance(player_score):
    player_name = list(player_score.keys())[0]
    player_total = sum(random.randint(1, 6) for _ in range(5))
    computer_total = sum(random.randint(1, 6) for _ in range(5))

    if player_total > computer_total:
        player_score[player_name] += 1
    elif computer_total > player_total:
        player_score['Computer'] = player_score.get('Computer', 0) + 1

    return player_score