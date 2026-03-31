import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money
    
    if spin_result % 2 == 0:  # spin result is even
        if 'even' in bets:
            total_money += bets['even']  # winnings from even bet
        if 'odd' in bets:
            total_money -= bets['odd']  # loss from odd bet
    else:  # spin result is odd
        if 'odd' in bets:
            total_money += bets['odd']  # winnings from odd bet
        if 'even' in bets:
            total_money -= bets['even']  # loss from even bet
    
    return total_money