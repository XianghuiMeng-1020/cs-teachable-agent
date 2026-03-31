import random

def simulate_game(players):
    scores = {}
    for player, dices in players.items():
        total_score = sum(random.randint(1, sides) for sides in dices)
        scores[player] = total_score
    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]
    return winners[0] if len(winners) == 1 else 'Tie'