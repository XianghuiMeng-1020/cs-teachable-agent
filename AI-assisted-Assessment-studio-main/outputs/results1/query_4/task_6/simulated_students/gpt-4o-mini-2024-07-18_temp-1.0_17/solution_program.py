import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money
    
    if spin_result % 2 == 0:  # Spin result is even
        if 'even' in bets:
            total_money += bets['even']  # Winning payout for even
        if 'odd' in bets:
            total_money -= bets['odd']  # Losing bet for odd
    else:  # Spin result is odd
        if 'odd' in bets:
            total_money += bets['odd']  # Winning payout for odd
        if 'even' in bets:
            total_money -= bets['even']  # Losing bet for even
    
    return total_money