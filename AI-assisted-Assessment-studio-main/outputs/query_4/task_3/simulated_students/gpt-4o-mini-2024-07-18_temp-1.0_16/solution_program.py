def calculate_player_scores(players, scores):
    total_scores = {}
    for i in range(len(players)):
        total_scores[players[i]] = sum(scores[i])
    return total_scores