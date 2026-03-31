def track_wins(games):
    victory_tracker = {}

    for game, winner in games:
        if winner not in victory_tracker:
            victory_tracker[winner] = {}
        if game not in victory_tracker[winner]:
            victory_tracker[winner][game] = 0
        victory_tracker[winner][game] += 1

    return victory_tracker