import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    final_money = money

    if spin_result % 2 == 0:  # If the result is even
        if 'even' in bets:
            win_amount = 2 * bets['even']
            final_money += win_amount - bets['even']
        if 'odd' in bets:
            final_money -= bets['odd']
    else:  # If the result is odd
        if 'odd' in bets:
            win_amount = 2 * bets['odd']
            final_money += win_amount - bets['odd']
        if 'even' in bets:
            final_money -= bets['even']

    return final_money