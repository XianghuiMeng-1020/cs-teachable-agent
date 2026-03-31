def update_leaderboard(score_entries):
    leaderboard = {}
    for entry in score_entries:
        parts = entry.split(',')
        if len(parts) != 2:
            continue
        player, score_str = parts[0].strip(), parts[1].strip()
        try:
            score = int(score_str)
            if player in leaderboard:
                leaderboard[player] += score
            else:
                leaderboard[player] = score
        except ValueError:
            continue
    return leaderboard