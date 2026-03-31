def check_game_winner(player_one_score, player_two_score):
    if player_one_score > player_two_score:
        return "Player One wins!"
    elif player_two_score > player_one_score:
        return "Player Two wins!"
    else:
        return "It's a tie!"