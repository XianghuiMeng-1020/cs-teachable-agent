def update_leaderboard(rounds):
    leaderboard = {}
    for game in rounds:
        for player, score in game.items():
            if player in leaderboard:
                leaderboard[player] += score
            else:
                leaderboard[player] = score
    sorted_leaderboard = dict(sorted(leaderboard.items(), key=lambda item: (-item[1], item[0])))
    return sorted_leaderboard