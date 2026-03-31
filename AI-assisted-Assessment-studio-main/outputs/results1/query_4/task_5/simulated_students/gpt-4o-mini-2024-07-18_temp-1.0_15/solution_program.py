import random

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0

    for i in range(rounds):
        bet_color, bet_amount = bets[i]
        if remaining_amount <= 0:
            break

        remaining_amount -= bet_amount

        outcome = random.randint(0, 1)  # 0 for 'red', 1 for 'black'
        winning_color = 'red' if outcome == 0 else 'black'

        if bet_color == winning_color:
            remaining_amount += bet_amount * 2  # Win: double the bet amount

        played_rounds += 1

    return {'remaining_amount': remaining_amount, 'played_rounds': played_rounds}