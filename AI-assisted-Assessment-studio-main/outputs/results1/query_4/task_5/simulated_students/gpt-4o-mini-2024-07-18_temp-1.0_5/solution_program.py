import random

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0

    for bet in bets:
        if played_rounds >= rounds or remaining_amount <= 0:
            break

        color, bet_amount = bet

        if bet_amount > remaining_amount:
            continue

        outcome = random.randint(0, 1)
        if (outcome == 0 and color == 'red') or (outcome == 1 and color == 'black'):
            remaining_amount += bet_amount
        else:
            remaining_amount -= bet_amount

        played_rounds += 1

    return {'remaining_amount': remaining_amount, 'played_rounds': played_rounds}