import random

def simulate_game(players):
    scores = {}
    for player, dice_sizes in players.items():
        total = sum(random.randint(1, sides) for sides in dice_sizes)
        scores[player] = total
    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]
    return 'Tie' if len(winners) > 1 else winners[0]