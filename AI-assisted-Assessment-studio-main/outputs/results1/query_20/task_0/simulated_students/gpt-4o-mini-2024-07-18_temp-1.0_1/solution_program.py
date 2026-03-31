def determine_turn_winner(player_1_name, player_1_score, player_2_name, player_2_score):
    if player_1_score > player_2_score:
        return player_1_name
    elif player_1_score < player_2_score:
        return player_2_name
    else:
        return "Draw"