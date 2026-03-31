import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money

    if spin_result % 2 == 0:
        if 'even' in bets:
            win = bets['even'] * 2
            total_money += win - bets['even']
        if 'odd' in bets:
            total_money -= bets['odd']
    else:
        if 'odd' in bets:
            win = bets['odd'] * 2
            total_money += win - bets['odd']
        if 'even' in bets:
            total_money -= bets['even']

    return total_money