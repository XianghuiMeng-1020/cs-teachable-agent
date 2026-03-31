import random


def balance_predictor(bets, initial_balance, outcome_probabilities):
    balance = initial_balance
    for bet in bets:
        probability, multiplier = outcome_probabilities[bet]
        # Simulate outcome
        dice_roll = random.randint(1, 100)
        if dice_roll <= probability:  # Player wins
            balance += 100 * multiplier
        else:  # Player loses
            balance -= 100
    return balance

# Example Usage
if __name__ == "__main__":
    bets = ['A', 'B', 'D']
    initial_balance = 1000
    probabilities = {
        'A': (50, 2),
        'B': (25, 3),
        'C': (75, 1.5),
        'D': (10, 5)
    }
    result = balance_predictor(bets, initial_balance, probabilities)
    print("Final balance:", result)