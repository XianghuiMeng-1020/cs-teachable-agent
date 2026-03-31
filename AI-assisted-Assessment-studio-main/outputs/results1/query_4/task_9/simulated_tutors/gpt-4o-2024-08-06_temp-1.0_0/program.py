import random

def game_of_chance(player_score):
    # Variables to hold game results
    player_total = 0
    computer_total = 0

    # Roll dice 5 times for both Player and Computer
    for _ in range(5):
        player_roll = random.randint(1, 6)
        computer_roll = random.randint(1, 6)
        player_total += player_roll
        computer_total += computer_roll

    # Determine winner and update scores in player_score dictionary
    if player_total > computer_total:
        # Assuming player's name is known, here taken as first key for simplicity
        player_name = list(player_score.keys())[0]
        player_score[player_name] += 1
    elif computer_total > player_total:
        if 'Computer' in player_score:
            player_score['Computer'] += 1
        else:
            player_score['Computer'] = 1
    # In case of tie, no operation needed

    return player_score
