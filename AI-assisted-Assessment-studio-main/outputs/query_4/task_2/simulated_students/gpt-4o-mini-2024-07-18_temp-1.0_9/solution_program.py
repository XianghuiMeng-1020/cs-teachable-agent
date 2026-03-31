def register_and_rank(players):
    game_scores = {}

    for player, info in players.items():
        game = info['game']
        score = info['score']
        if game not in game_scores:
            game_scores[game] = []
        game_scores[game].append((player, score))

    results = {}
    for game, entries in game_scores.items():
        entries.sort(key=lambda x: x[1], reverse=True)
        highest_scorer = entries[0][0]
        leaderboard = [entry[0] for entry in entries]
        results[game] = (highest_scorer, leaderboard)

    return results