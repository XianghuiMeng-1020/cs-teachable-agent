import random

def simulate_game(players):
    scores = {}
    max_score = 0
    winners = []
    
    for player, dice in players.items():
        total_score = 0
        for sides in dice:
            total_score += random.randint(1, sides)
        scores[player] = total_score
        
        if total_score > max_score:
            max_score = total_score
            winners = [player]
        elif total_score == max_score:
            winners.append(player)

    return 'Tie' if len(winners) > 1 else winners[0]