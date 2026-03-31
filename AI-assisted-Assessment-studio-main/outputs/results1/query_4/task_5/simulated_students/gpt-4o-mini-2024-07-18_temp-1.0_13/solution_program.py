import random

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0

    for i in range(rounds):
        color, bet_amount = bets[i]
        if remaining_amount <= 0:
            break
        
        # Simulating the outcome
        outcome = random.randint(0, 1)  # 0 for 'red', 1 for 'black'
        if (color == 'red' and outcome == 0) or (color == 'black' and outcome == 1):
            remaining_amount += bet_amount  # Win
        else:
            remaining_amount -= bet_amount  # Loss

        played_rounds += 1

    return {'remaining_amount': remaining_amount, 'played_rounds': played_rounds}