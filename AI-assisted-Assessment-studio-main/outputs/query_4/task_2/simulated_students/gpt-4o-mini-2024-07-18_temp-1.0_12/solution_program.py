def register_and_rank(players):
    game_data = {}
    
    for player, info in players.items():
        game = info['game']
        score = info['score']
        
        if game not in game_data:
            game_data[game] = []
        game_data[game].append((player, score))
    
    result = {}
    for game, scores in game_data.items():
        scores.sort(key=lambda x: x[1], reverse=True)
        highest_player = scores[0][0]
        leaderboard = [player for player, score in scores]
        result[game] = (highest_player, leaderboard)
    
    return result