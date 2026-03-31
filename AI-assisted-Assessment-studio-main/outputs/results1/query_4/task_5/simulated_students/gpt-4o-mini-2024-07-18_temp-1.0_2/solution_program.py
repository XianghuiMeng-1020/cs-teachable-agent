import random

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0

    for i in range(rounds):
        bet_color, bet_amount = bets[i]
        if remaining_amount <= 0:
            break
        remaining_amount -= bet_amount
        outcome = random.randint(0, 1)
        if (outcome == 0 and bet_color == 'red') or (outcome == 1 and bet_color == 'black'):
            remaining_amount += bet_amount * 2
        played_rounds += 1

    return {'remaining_amount': remaining_amount, 'played_rounds': played_rounds}