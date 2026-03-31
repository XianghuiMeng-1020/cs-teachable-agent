def calculate_player_scores(players, scores):
    score_dict = {}
    for player, score_list in zip(players, scores):
        score_dict[player] = sum(score_list)
    return score_dict