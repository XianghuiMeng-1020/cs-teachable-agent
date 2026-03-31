import random

def simulate_game(player_dice):
    scores = {}
    
    for player, dice in player_dice.items():
        total_score = 0
        for sides in dice:
            total_score += random.randint(1, sides)
        scores[player] = total_score
    
    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]
    
    if len(winners) == 1:
        return winners[0]
    else:
        return 'Tie'