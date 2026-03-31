def update_leaderboard(score_entries):
    leaderboard = {}

    for entry in score_entries:
        parts = entry.split(',', 1)  # Split only on the first comma
        if len(parts) != 2:
            continue  # Skip malformed entries
        player_name, score_str = parts
        player_name = player_name.strip()
        score_str = score_str.strip()

        try:
            score = int(score_str)
        except ValueError:
            continue  # Skip if score is not an integer

        if player_name in leaderboard:
            leaderboard[player_name] += score
        else:
            leaderboard[player_name] = score

    return leaderboard