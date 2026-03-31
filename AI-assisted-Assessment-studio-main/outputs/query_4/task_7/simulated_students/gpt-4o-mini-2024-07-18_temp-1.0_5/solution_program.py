def track_wins(games):
    wins = {}
    for game, winner in games:
        if winner not in wins:
            wins[winner] = {}
        if game not in wins[winner]:
            wins[winner][game] = 0
        wins[winner][game] += 1
    return wins