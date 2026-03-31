def update_leaderboard(score_entries):
    leaderboard = {}
    
    for entry in score_entries:
        if entry.count(',') != 1:
            continue  # Skip malformed entries
        name, score_str = entry.split(',', 1)
        try:
            score = int(score_str)
        except ValueError:
            continue  # Skip entries with invalid scores
        
        if name in leaderboard:
            leaderboard[name] += score
        else:
            leaderboard[name] = score
    
    return leaderboard