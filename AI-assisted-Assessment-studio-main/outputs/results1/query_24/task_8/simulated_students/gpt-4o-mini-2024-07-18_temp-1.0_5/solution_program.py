def update_leaderboard(score_entries):
    leaderboard = {}
    for entry in score_entries:
        parts = entry.split(',')
        if len(parts) != 2:
            continue
        player_name = parts[0].strip()
        try:
            score = int(parts[1].strip())
        except ValueError:
            continue
        if player_name in leaderboard:
            leaderboard[player_name] += score
        else:
            leaderboard[player_name] = score
    return leaderboard