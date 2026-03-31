def update_leaderboard(rounds):
    leaderboard = {}

    for round_scores in rounds:
        for player, points in round_scores.items():
            if player not in leaderboard:
                leaderboard[player] = 0
            leaderboard[player] += points

    sorted_leaderboard = dict(sorted(leaderboard.items(), key=lambda item: (-item[1], item[0])))
    return sorted_leaderboard