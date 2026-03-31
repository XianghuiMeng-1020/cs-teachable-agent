def register_and_rank(players):
    game_scores = {}
    for player, info in players.items():
        game = info['game']
        score = info['score']
        if game not in game_scores:
            game_scores[game] = []
        game_scores[game].append((player, score))
    results = {}
    for game, scores in game_scores.items():
        scores.sort(key=lambda x: x[1], reverse=True)
        top_player = scores[0][0]
        leaderboard = [player for player, score in scores]
        results[game] = (top_player, leaderboard)
    return results