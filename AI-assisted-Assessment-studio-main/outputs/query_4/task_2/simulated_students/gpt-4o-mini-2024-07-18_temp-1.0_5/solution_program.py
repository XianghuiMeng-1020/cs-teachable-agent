def register_and_rank(players):
    game_data = {}

    for player, details in players.items():
        game = details['game']
        score = details['score']

        if game not in game_data:
            game_data[game] = {'highest_score': score, 'top_player': player, 'leaderboard': []}
        else:
            if score > game_data[game]['highest_score']:
                game_data[game]['highest_score'] = score
                game_data[game]['top_player'] = player

        game_data[game]['leaderboard'].append((player, score))

    result = {}

    for game, data in game_data.items():
        leaderboard = sorted(data['leaderboard'], key=lambda x: x[1], reverse=True)
        sorted_leaderboard = [player[0] for player in leaderboard]
        result[game] = (data['top_player'], sorted_leaderboard)

    return result