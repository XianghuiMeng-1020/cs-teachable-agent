import random

def lucky_draw_game(player_numbers):
    score = 0
    game_results = {}

    for round_number, player_number in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        round_result = {
            'player_guess': player_number,
            'winning_number': winning_number
        }
        game_results[round_number] = round_result
        if player_number == winning_number:
            score += 10

    return score