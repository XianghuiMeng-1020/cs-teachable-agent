def register_and_rank(players):
    game_scores = {}
    leaderboard = {}

    for player, info in players.items():
        game = info['game']
        score = info['score']

        if game not in game_scores:
            game_scores[game] = score
            leaderboard[game] = [(player, score)]
        else:
            if score > game_scores[game]:
                game_scores[game] = score
            leaderboard[game].append((player, score))

    result = {}
    for game in leaderboard:
        leaderboard[game].sort(key=lambda x: x[1], reverse=True)
        highest_player = leaderboard[game][0][0]
        sorted_leaderboard = [player[0] for player in leaderboard[game]]
        result[game] = (highest_player, sorted_leaderboard)

    return result