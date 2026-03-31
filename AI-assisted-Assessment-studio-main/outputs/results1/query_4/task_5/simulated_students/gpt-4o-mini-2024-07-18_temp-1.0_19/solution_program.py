import random

def play_roulette(starting_amount, rounds, bets):
    current_amount = starting_amount
    played_rounds = 0

    for i in range(rounds):
        if played_rounds < len(bets):
            color, bet_amount = bets[played_rounds]
            if bet_amount > current_amount:
                break
            outcome = random.randint(0, 1)
            if (outcome == 0 and color == 'red') or (outcome == 1 and color == 'black'):
                current_amount += bet_amount
            else:
                current_amount -= bet_amount
            played_rounds += 1
        else:
            break

    return {'remaining_amount': current_amount, 'played_rounds': played_rounds}