import random

def game_of_chance(player_score):
    player_name = list(player_score.keys())[0]
    player_sum = sum(random.randint(1, 6) for _ in range(5))
    computer_sum = sum(random.randint(1, 6) for _ in range(5))

    if player_sum > computer_sum:
        player_score[player_name] += 1
    elif computer_sum > player_sum:
        player_score['Computer'] = player_score.get('Computer', 0) + 1

    return player_score