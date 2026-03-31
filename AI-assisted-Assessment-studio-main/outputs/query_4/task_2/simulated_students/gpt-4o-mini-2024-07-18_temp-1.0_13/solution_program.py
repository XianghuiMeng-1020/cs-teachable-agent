def register_and_rank(players):
    games = {}

    for player, info in players.items():
        game = info['game']
        score = info['score']

        if game not in games:
            games[game] = []
        games[game].append((player, score))

    leaderboard = {}

    for game, scores in games.items():
        scores.sort(key=lambda x: x[1], reverse=True)
        highest_scorer = scores[0][0]
        leaderboard_list = [player for player, score in scores]
        leaderboard[game] = (highest_scorer, leaderboard_list)

    return leaderboard