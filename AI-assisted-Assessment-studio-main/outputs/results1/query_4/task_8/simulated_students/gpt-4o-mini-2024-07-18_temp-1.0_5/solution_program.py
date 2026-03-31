import random

def lucky_draw_game(player_numbers):
    total_score = 0
    rounds = {}

    for i, guess in enumerate(player_numbers):
        round_number = i + 1
        winning_number = random.randint(1, 5)
        rounds[round_number] = {'guessed_number': guess, 'winning_number': winning_number}
        if guess == winning_number:
            total_score += 10

    return total_score
