def score_board_games(players, games):
    for game in games:
        winner = game['winner']
        players[winner] += 10