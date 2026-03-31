import random

def lucky_draw_game(player_numbers):
    score = 0
    results = {}
    for i, guess in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        round_result = {
            'player_guess': guess,
            'winning_number': winning_number
        }
        results[i] = round_result
        if guess == winning_number:
            score += 10
    return score
