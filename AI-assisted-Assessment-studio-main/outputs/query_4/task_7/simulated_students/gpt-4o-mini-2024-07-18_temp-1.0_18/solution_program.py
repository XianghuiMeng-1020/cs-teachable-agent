def track_wins(games):
    results = {}
    
    for game_name, winner_name in games:
        if winner_name not in results:
            results[winner_name] = {}
        if game_name not in results[winner_name]:
            results[winner_name][game_name] = 0
        results[winner_name][game_name] += 1
    
    # Filter out players with no wins
    return {player: wins for player, wins in results.items() if sum(wins.values()) > 0}