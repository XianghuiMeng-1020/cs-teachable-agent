def update_leaderboard(score_entries):
    leaderboard = {}
    for entry in score_entries:
        parts = entry.split(',')
        if len(parts) != 2:
            continue
        name = parts[0].strip()
        try:
            score = int(parts[1].strip())
        except ValueError:
            continue
        if name in leaderboard:
            leaderboard[name] += score
        else:
            leaderboard[name] = score
    return leaderboard