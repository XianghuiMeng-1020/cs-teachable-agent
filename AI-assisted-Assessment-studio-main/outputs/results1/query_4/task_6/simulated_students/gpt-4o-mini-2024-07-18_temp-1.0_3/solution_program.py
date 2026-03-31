import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money

    if spin_result % 2 == 0:  # result is even
        if 'even' in bets:
            total_money += bets['even']  # win on even
            if bets['even'] > 0:
                total_money += bets['even']  # double the bet
        if 'odd' in bets:
            total_money -= bets['odd']  # lose on odd
    else:  # result is odd
        if 'odd' in bets:
            total_money += bets['odd']  # win on odd
            if bets['odd'] > 0:
                total_money += bets['odd']  # double the bet
        if 'even' in bets:
            total_money -= bets['even']  # lose on even

    return total_money