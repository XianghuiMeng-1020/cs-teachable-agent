import random

def play_roulette(starting_amount, rounds, bets):
    amount = starting_amount
    played_rounds = 0
    
    for i in range(rounds):
        color, bet = bets[i]
        if amount <= 0:
            break
        outcome = random.randint(0, 1)
        if (color == 'red' and outcome == 0) or (color == 'black' and outcome == 1):
            amount += bet
        else:
            amount -= bet
        played_rounds += 1
    
    return {'remaining_amount': amount, 'played_rounds': played_rounds}