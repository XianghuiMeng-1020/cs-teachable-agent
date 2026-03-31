def register_and_rank(players):
    game_scores = {}

    for player, details in players.items():
        game = details['game']
        score = details['score']
        if game not in game_scores:
            game_scores[game] = []
        game_scores[game].append((player, score))

    result = {}

    for game, scores in game_scores.items():
        scores.sort(key=lambda x: x[1], reverse=True)
        highest_player = scores[0][0]
        leaderboard = [player for player, score in scores]
        result[game] = (highest_player, leaderboard)

    return result