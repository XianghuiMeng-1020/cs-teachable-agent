import random

def simulate_game(players):
    totals = {}
    for player, dice in players.items():
        total = sum(random.randint(1, sides) for sides in dice)
        totals[player] = total
    max_score = max(totals.values())
    winners = [player for player, score in totals.items() if score == max_score]
    return winners[0] if len(winners) == 1 else 'Tie'