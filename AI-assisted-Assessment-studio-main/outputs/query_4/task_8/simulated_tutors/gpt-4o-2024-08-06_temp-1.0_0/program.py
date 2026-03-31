def calculate_final_scores(game_log):
    final_scores = {}
    for player, changes in game_log.items():
        score = 0
        for change in changes:
            score += change
            if score < 0:
                score = 0
        final_scores[player] = score
    return final_scores

# Sample usage:
game_log = {'Alice': [10, -5, 20, -30, 5], 'Bob': [-10, 20, 15, -5, 10]}
print(calculate_final_scores(game_log))  # Output: {'Alice': 5, 'Bob': 30}