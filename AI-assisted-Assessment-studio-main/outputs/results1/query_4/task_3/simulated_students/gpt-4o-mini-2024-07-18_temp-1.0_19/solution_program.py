import random

def simulate_game(players):
    scores = {}
    for player, dice in players.items():
        total = sum(random.randint(1, sides) for sides in dice)
        scores[player] = total

    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]

    if len(winners) > 1:
        return 'Tie'
    return winners[0]