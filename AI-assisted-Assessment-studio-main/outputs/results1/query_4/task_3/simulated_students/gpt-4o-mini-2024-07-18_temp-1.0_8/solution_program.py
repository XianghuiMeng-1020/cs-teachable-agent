import random

def simulate_game(player_dict):
    scores = {}
    for player, dice in player_dict.items():
        total = 0
        for sides in dice:
            total += random.randint(1, sides)
        scores[player] = total
    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]
    return winners[0] if len(winners) == 1 else 'Tie'