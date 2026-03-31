import random

def lucky_draw_game(player_numbers):
    total_score = 0
    rounds = {}
    
    for round_number, player_guess in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        round_result = {
            'player_guess': player_guess,
            'winning_number': winning_number
        }
        rounds[round_number] = round_result
        
        if player_guess == winning_number:
            total_score += 10
    
    return total_score