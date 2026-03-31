import random

def lucky_draw_game(player_numbers):
    total_score = 0
    game_results = {}
    
    for round_number, player_guess in enumerate(player_numbers, start=1):
        winning_number = random.randint(1, 5)
        round_score = 10 if player_guess == winning_number else 0
        total_score += round_score
        game_results[round_number] = {'player_guess': player_guess, 'winning_number': winning_number}
    
    return total_score