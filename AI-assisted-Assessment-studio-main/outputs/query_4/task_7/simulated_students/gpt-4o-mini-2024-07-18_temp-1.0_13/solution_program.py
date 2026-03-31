def track_wins(games):
    wins = {}

    for game_name, winner_name in games:
        if winner_name not in wins:
            wins[winner_name] = {}
        if game_name not in wins[winner_name]:
            wins[winner_name][game_name] = 0
        wins[winner_name][game_name] += 1

    return wins