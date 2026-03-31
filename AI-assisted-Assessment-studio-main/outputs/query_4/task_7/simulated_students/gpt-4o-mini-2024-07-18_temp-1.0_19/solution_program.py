def track_wins(games):
    win_tracker = {}
    for game_name, winner_name in games:
        if winner_name not in win_tracker:
            win_tracker[winner_name] = {}
        if game_name not in win_tracker[winner_name]:
            win_tracker[winner_name][game_name] = 0
        win_tracker[winner_name][game_name] += 1
    return win_tracker