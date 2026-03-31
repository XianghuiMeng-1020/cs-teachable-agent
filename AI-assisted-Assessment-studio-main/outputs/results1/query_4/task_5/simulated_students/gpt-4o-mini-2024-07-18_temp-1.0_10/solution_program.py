import random

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0

    for i in range(min(rounds, len(bets))):
        color, bet_amount = bets[i]
        if remaining_amount == 0:
            break
        if bet_amount > remaining_amount:
            break
        outcome = random.randint(0, 1)
        if (color == 'red' and outcome == 0) or (color == 'black' and outcome == 1):
            remaining_amount += bet_amount
        else:
            remaining_amount -= bet_amount
        played_rounds += 1

    return {'remaining_amount': remaining_amount, 'played_rounds': played_rounds}