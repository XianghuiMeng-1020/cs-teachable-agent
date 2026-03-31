def calculate_player_scores(players, scores):
    return {players[i]: sum(scores[i]) for i in range(len(players))}