import random

def lucky_draw_game(player_numbers):
    score = 0
    rounds = {}

    for i, guess in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        rounds[i] = {'player_guess': guess, 'winning_number': winning_number}
        if guess == winning_number:
            score += 10

    return score