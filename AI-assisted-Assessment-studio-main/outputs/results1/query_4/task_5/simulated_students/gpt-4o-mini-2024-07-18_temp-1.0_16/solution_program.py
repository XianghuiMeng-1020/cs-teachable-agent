import random

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0

    for i in range(rounds):
        bet_color, bet_amount = bets[i]
        if remaining_amount <= 0:
            break
        played_rounds += 1
        # Simulate the result of the round
        spin_result = random.randint(0, 1)  # 0 for 'red', 1 for 'black'
        if (spin_result == 0 and bet_color == 'red') or 
           (spin_result == 1 and bet_color == 'black'):
            remaining_amount += bet_amount  # Win
        else:
            remaining_amount -= bet_amount  # Lose

    return {'remaining_amount': remaining_amount, 'played_rounds': played_rounds}