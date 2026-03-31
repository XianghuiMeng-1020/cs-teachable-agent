def calculate_player_scores(players, scores):
    player_scores = {}
    for i in range(len(players)):
        total_score = 0
        for score in scores[i]:
            total_score += score
        player_scores[players[i]] = total_score
    return player_scores