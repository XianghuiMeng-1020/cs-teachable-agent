import random

def simulate_game(players):
    # Dictionary to store the sum of roll outcomes for each player
    outcomes = {}
    
    # Iterate through each player and their list of dice
    for player, dice in players.items():
        # Calculate the sum of random roll outcomes for player's dice
        total = sum(random.randint(1, sides) for sides in dice)
        outcomes[player] = total
    
    # Determine the highest roll sum
    highest_sum = max(outcomes.values())
    # Find all players with this highest sum
    winners = [player for player, total in outcomes.items() if total == highest_sum]
    
    # Determine winner or tie
    if len(winners) == 1:
        return winners[0]
    else:
        return "Tie"
