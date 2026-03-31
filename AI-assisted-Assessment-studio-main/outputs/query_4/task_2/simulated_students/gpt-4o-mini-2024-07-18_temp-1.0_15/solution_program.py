def register_and_rank(players):
    game_scores = {}
    game_leaderboard = {}

    for player, data in players.items():
        game = data['game']
        score = data['score']

        if game not in game_scores:
            game_scores[game] = score
            game_leaderboard[game] = [player]
        else:
            if score > game_scores[game]:
                game_scores[game] = score
                game_leaderboard[game] = [player]
            elif score == game_scores[game]:
                game_leaderboard[game].append(player)
            game_leaderboard[game].append(player)

    result = {}
    for game, highest_score in game_scores.items():
        players_in_game = [player for player, data in players.items() if data['game'] == game]
        sorted_leaderboard = sorted(players_in_game, key=lambda p: -players[p]['score'])
        result[game] = (sorted_leaderboard[0], sorted_leaderboard)

    return result