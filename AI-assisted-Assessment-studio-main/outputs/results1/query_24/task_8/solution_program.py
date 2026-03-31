def update_leaderboard(score_entries):
    leaderboard = {}
    
    for entry in score_entries:
        try:
            player, score = entry.split(',')
            score = int(score)
            if player in leaderboard:
                leaderboard[player] += score
            else:
                leaderboard[player] = score
        except (ValueError, IndexError):
            continue
        
    return leaderboard