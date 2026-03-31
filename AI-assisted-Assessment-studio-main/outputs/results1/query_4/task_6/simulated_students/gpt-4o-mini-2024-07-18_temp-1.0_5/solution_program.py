import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money

    if spin_result % 2 == 0:
        outcome = 'even'
    else:
        outcome = 'odd'

    for bet_type, bet_amount in bets.items():
        if bet_type == 'even' and outcome == 'even':
            total_money += bet_amount  # Winning the even bet
        elif bet_type == 'odd' and outcome == 'odd':
            total_money += bet_amount  # Winning the odd bet
        else:
            total_money -= bet_amount  # Losing the bet

    return total_money