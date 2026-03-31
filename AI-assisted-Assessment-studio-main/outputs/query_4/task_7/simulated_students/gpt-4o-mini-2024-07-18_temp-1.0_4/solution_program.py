def track_wins(games):
    victory_tracker = {}

    for game_name, winner_name in games:
        if winner_name not in victory_tracker:
            victory_tracker[winner_name] = {}
        if game_name not in victory_tracker[winner_name]:
            victory_tracker[winner_name][game_name] = 0
        victory_tracker[winner_name][game_name] += 1

    return victory_tracker