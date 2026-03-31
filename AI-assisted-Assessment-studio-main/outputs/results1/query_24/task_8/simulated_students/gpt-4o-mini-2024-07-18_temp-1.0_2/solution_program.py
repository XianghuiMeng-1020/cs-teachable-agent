def update_leaderboard(score_entries):
    leaderboard = {}
    for entry in score_entries:
        parts = entry.split(',')
        if len(parts) != 2:
            continue
        player, score_str = parts
        try:
            score = int(score_str)
        except ValueError:
            continue
        if player in leaderboard:
            leaderboard[player] += score
        else:
            leaderboard[player] = score
    return leaderboard