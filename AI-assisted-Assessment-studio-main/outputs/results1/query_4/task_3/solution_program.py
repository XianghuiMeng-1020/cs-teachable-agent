from random import randint

def simulate_game(players):
    scores = {}
    for player, dice in players.items():
        total_score = 0
        for die in dice:
            total_score += randint(1, die)
        scores[player] = total_score
    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]
    if len(winners) > 1:
        return "Tie"
    else:
        return winners[0]