import random

def game_of_chance(player_score):
    player_rolls = [random.randint(1, 6) for _ in range(5)]
    computer_rolls = [random.randint(1, 6) for _ in range(5)]
    player_total = sum(player_rolls)
    computer_total = sum(computer_rolls)

    if player_total > computer_total:
        player_score[list(player_score.keys())[0]] += 1
    elif computer_total > player_total:
        if "Computer" in player_score:
            player_score["Computer"] += 1
        else:
            player_score["Computer"] = 1

    return player_score