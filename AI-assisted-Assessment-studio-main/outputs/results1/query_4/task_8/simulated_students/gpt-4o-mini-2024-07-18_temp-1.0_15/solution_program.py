import random

def lucky_draw_game(player_numbers):
    total_score = 0
    results = {}

    for round_num, player_number in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        if player_number < 1 or player_number > 5:
            raise ValueError('Player number must be between 1 and 5')
        if winning_number == player_number:
            total_score += 10
        results[round_num] = {'player_number': player_number, 'winning_number': winning_number}

    return total_score