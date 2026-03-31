import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money
    
    if spin_result % 2 == 0:
        if 'even' in bets:
            total_money += bets['even']  # Win on even
        if 'odd' in bets:
            total_money -= bets['odd']  # Lose on odd
    else:
        if 'odd' in bets:
            total_money += bets['odd']  # Win on odd
        if 'even' in bets:
            total_money -= bets['even']  # Lose on even
    
    return total_money