import random

def lucky_draw_game(player_numbers):
    rounds = {}
    total_score = 0
    for round_number, player_number in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        round_data = {
            'player_guess': player_number,
            'winning_number': winning_number
        }
        if player_number == winning_number:
            total_score += 10
        # Store each round's data into the rounds dictionary
        rounds[round_number] = round_data
    return total_score