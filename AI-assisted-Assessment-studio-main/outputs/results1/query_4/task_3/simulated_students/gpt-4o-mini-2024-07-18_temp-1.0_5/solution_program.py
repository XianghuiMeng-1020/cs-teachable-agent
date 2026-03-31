import random

def simulate_game(player_dice):
    scores = {}
    for player, dice_sides in player_dice.items():
        total_score = sum(random.randint(1, sides) for sides in dice_sides)
        scores[player] = total_score
    
    max_score = max(scores.values())
    winners = [player for player, score in scores.items() if score == max_score]
    
    if len(winners) == 1:
        return winners[0]
    else:
        return 'Tie'