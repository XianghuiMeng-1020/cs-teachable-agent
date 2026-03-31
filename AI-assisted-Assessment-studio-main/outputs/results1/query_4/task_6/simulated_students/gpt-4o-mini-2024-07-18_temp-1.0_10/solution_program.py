import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    if spin_result % 2 == 0:
        outcome = 'even'
    else:
        outcome = 'odd'

    total_money = money
    for bet_type, bet_amount in bets.items():
        if bet_type == outcome:
            total_money += bet_amount  # Win, receive double
        else:
            total_money -= bet_amount  # Lose, lose the bet

    return total_money