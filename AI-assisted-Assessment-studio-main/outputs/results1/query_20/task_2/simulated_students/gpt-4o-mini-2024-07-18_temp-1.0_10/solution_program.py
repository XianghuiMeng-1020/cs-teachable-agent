def chess_game_outcome(score_player1, score_player2, player1_name, player2_name):
    if score_player1 > score_player2:
        return player1_name + ' is victorious!'
    elif score_player2 > score_player1:
        return player2_name + ' is victorious!'
    else:
        return 'The game is a draw!'}