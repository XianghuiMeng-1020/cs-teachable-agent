import random

def lucky_draw_game(player_numbers):
    score = 0
    results = {}
    
    for round_number, player_number in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        results[round_number] = {'player_guess': player_number, 'winning_number': winning_number}
        if player_number == winning_number:
            score += 10
    
    return score