def update_leaderboard(rounds):
    leaderboard = {}
    
    for round in rounds:
        for player, points in round.items():
            if player in leaderboard:
                leaderboard[player] += points
            else:
                leaderboard[player] = points
    
    sorted_leaderboard = dict(sorted(leaderboard.items(), key=lambda item: (-item[1], item[0])))
    return sorted_leaderboard