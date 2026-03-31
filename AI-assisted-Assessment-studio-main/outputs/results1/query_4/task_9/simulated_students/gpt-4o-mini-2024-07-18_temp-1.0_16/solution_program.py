import random

def game_of_chance(player_score):
    player_rolls = [random.randint(1, 6) for _ in range(5)]
    computer_rolls = [random.randint(1, 6) for _ in range(5)]
    player_total = sum(player_rolls)
    computer_total = sum(computer_rolls)

    if player_total > computer_total:
        player_name = list(player_score.keys())[0]
        player_score[player_name] += 1
    elif computer_total > player_total:
        player_score['Computer'] = player_score.get('Computer', 0) + 1

    return player_score