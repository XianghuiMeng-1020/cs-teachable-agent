import random

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0

    for bet_color, bet_amount in bets:
        # Terminate if funds are not enough or no more rounds left
        if remaining_amount <= 0 or played_rounds >= rounds:
            break
        
        # Simulate a round
        winning_color = 'red' if random.randint(0, 1) == 0 else 'black'

        # Determine the outcome of the bet
        if bet_color == winning_color:
            remaining_amount += bet_amount  # Win: Double the bet amount
        else:
            remaining_amount -= bet_amount  # Loss: Lose the bet amount

        # Increment the number of played rounds
        played_rounds += 1

    return {
        'remaining_amount': remaining_amount,
        'played_rounds': played_rounds
    }

# Example usage
result = play_roulette(100, 5, [('red', 10), ('black', 20), ('red', 30), ('black', 40), ('red', 50)])
print(result)