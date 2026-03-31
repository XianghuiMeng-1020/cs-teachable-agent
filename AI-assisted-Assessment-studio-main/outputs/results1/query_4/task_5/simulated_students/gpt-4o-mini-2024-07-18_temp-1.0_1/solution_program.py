import random

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0

    for round_ in range(rounds):
        bet_color, bet_amount = bets[round_]
        if remaining_amount <= 0:
            break

        winning_color = random.choice(['red', 'black'])
        if bet_color == winning_color:
            remaining_amount += bet_amount
        else:
            remaining_amount -= bet_amount

        played_rounds += 1

    return {'remaining_amount': remaining_amount, 'played_rounds': played_rounds}