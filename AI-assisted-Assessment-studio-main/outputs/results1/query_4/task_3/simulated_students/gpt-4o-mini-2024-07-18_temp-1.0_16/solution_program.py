import random

def simulate_game(players):
    results = {}

    for player, dice in players.items():
        total_sum = 0
        for sides in dice:
            total_sum += random.randint(1, sides)
        results[player] = total_sum

    max_score = max(results.values())
    winners = [player for player, score in results.items() if score == max_score]

    if len(winners) > 1:
        return 'Tie'
    else:
        return winners[0]