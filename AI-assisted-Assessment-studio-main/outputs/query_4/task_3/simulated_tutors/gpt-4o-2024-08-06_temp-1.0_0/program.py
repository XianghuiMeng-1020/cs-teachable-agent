def calculate_player_scores(players, scores):
    # Initialize an empty dictionary to store the total scores for each player
    player_scores = {}
    
    # Iterate through each player and their corresponding scores
    for i, player in enumerate(players):
        # Calculate the total score for the player
        total_score = sum(scores[i])
        # Add the player's name and their total score to the dictionary
        player_scores[player] = total_score
    
    return player_scores

# Example usage:
players = ['Alice', 'Bob', 'Charlie']
scores = [[10, 20, 30], [15, 25], [5, 10, 5, 10]]
print(calculate_player_scores(players, scores))  # Output: {'Alice': 60, 'Bob': 40, 'Charlie': 30}