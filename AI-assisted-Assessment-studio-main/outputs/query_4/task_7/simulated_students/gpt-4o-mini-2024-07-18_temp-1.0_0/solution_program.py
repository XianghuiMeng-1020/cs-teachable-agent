def track_wins(games):
    win_tracker = {}
    
    for game, winner in games:
        if winner not in win_tracker:
            win_tracker[winner] = {}
        if game not in win_tracker[winner]:
            win_tracker[winner][game] = 0
        win_tracker[winner][game] += 1
    
    return win_tracker