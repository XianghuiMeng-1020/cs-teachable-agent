def calculate_player_scores(players, scores):
    player_scores = {}
    for player, score_list in zip(players, scores):
        player_scores[player] = sum(score_list)
    return player_scores