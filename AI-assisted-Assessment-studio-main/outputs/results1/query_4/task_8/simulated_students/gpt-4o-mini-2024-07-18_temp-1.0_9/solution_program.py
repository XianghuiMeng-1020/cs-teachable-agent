import random

def lucky_draw_game(player_numbers):
    score = 0
    rounds = {}
    
    for round_number, player_guess in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        
        if player_guess == winning_number:
            score += 10
        
        rounds[round_number] = {
            'player_guess': player_guess,
            'winning_number': winning_number
        }
    
    return score