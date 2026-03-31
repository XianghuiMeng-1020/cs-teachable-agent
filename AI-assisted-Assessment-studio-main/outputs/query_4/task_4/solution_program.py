def score_board_games(players, games):
    for game in games:
        winner = game.get("winner")
        if winner in players:
            players[winner] = players[winner] + 10