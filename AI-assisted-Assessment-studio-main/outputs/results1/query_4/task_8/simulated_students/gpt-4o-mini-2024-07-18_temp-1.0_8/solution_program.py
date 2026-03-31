import random

def lucky_draw_game(player_numbers):
    total_score = 0
    results = {}

    for round_number, guess in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        round_result = {
            'player_guess': guess,
            'winning_number': winning_number
        }
        results[round_number] = round_result
        if guess == winning_number:
            total_score += 10

    return total_score