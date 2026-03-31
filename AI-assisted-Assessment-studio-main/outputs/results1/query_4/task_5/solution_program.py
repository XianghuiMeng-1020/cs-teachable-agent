import random

random.seed(0)

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0
    for i in range(min(rounds, len(bets))):
        bet_color, bet_amount = bets[i]
        if remaining_amount == 0:
            break
        if random.randint(0, 1) == 0:
            winner = 'red'
        else:
            winner = 'black'
        if bet_color == winner:
            remaining_amount += bet_amount
        else:
            remaining_amount -= bet_amount
        played_rounds += 1
    return {'remaining_amount': remaining_amount, 'played_rounds': played_rounds}