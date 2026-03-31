def register_and_rank(players):
    game_scores = {}
    game_leaders = {}

    for player, details in players.items():
        game = details['game']
        score = details['score']

        if game not in game_scores:
            game_scores[game] = []
        game_scores[game].append((player, score))

    for game, scores in game_scores.items():
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        highest_scorer = sorted_scores[0][0]
        leaderboard = [player for player, score in sorted_scores]
        game_leaders[game] = (highest_scorer, leaderboard)

    return game_leaders