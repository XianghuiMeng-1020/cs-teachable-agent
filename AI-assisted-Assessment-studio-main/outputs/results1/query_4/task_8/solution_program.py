import random

def lucky_draw_game(player_numbers):
    total_score = 0
    game_rounds = {}
    for round_number, player_number in enumerate(player_numbers, 1):
        winning_number = random.randint(1, 5)
        round_result = {
            "player_guess": player_number,
            "winning_number": winning_number
        }
        if player_number == winning_number:
            total_score += 10
        game_rounds[round_number] = round_result
    return total_score