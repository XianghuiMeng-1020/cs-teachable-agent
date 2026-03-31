def register_and_rank(players):
    games = {}
    for player, details in players.items():
        game = details['game']
        score = details['score']
        if game not in games:
            games[game] = {}
        games[game][player] = score

    results = {}
    for game, player_scores in games.items():
        sorted_players = sorted(player_scores.items(), key=lambda x: x[1], reverse=True)
        top_player = sorted_players[0][0]
        leaderboard = [name for name, score in sorted_players]
        results[game] = (top_player, leaderboard)
    return results