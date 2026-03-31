import random

def simulate_game(player_dice):
    scores = {}
    for player, sides in player_dice.items():
        total_score = sum(random.randint(1, side) for side in sides)
        scores[player] = total_score
    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]
    return winners[0] if len(winners) == 1 else 'Tie'