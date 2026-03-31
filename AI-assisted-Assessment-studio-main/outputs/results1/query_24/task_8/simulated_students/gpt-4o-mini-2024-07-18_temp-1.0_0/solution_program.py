def update_leaderboard(score_entries):
    leaderboard = {}
    for entry in score_entries:
        parts = entry.split(',')
        if len(parts) != 2:
            continue
        player = parts[0].strip()
        try:
            score = int(parts[1].strip())
        except ValueError:
            continue
        if player in leaderboard:
            leaderboard[player] += score
        else:
            leaderboard[player] = score
    return leaderboard