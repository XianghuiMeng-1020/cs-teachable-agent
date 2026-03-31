import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money

    if spin_result % 2 == 0:
        if 'even' in bets:
            winnings = bets['even'] * 2
            total_money += winnings - bets['even']
        if 'odd' in bets:
            total_money -= bets['odd']
    else:
        if 'odd' in bets:
            winnings = bets['odd'] * 2
            total_money += winnings - bets['odd']
        if 'even' in bets:
            total_money -= bets['even']

    return total_money