def register_and_rank(players):
    game_data = {}

    for player, info in players.items():
        game = info['game']
        score = info['score']
        
        if game not in game_data:
            game_data[game] = []
        game_data[game].append((player, score))

    result = {}
    for game, player_scores in game_data.items():
        player_scores.sort(key=lambda x: x[1], reverse=True)
        highest_scorer = player_scores[0][0]
        leaderboard = [player[0] for player in player_scores]
        result[game] = (highest_scorer, leaderboard)

    return result