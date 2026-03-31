def register_and_rank(players):
    # Initialize dictionaries to store scores and leaderboards for each game
    scores = {'Chess': [], 'Scrabble': [], 'Monopoly': []}
    leaderboards = {'Chess': [], 'Scrabble': [], 'Monopoly': []}
    
    # Populate scores dictionary with player information
    for player, info in players.items():
        game = info['game']
        scores[game].append((player, info['score']))
        
    # Process each game's leaderboard
    result = {}
    for game, score_list in scores.items():
        # Sort players by score in descending order
        sorted_players = sorted(score_list, key=lambda x: x[1], reverse=True)

        # Find the highest scoring player for each game
        highest_scoring_player = sorted_players[0][0]

        # Create leaderboard for the game
        leaderboard = [player for player, _ in sorted_players]

        # Store the result for that game
        result[game] = (highest_scoring_player, leaderboard)

    return result

# Example usage
players = {
    'Alice': {'game': 'Chess', 'score': 200},
    'Bob': {'game': 'Scrabble', 'score': 300},
    'Cathy': {'game': 'Chess', 'score': 250},
    'David': {'game': 'Monopoly', 'score': 150},
}

print(register_and_rank(players))