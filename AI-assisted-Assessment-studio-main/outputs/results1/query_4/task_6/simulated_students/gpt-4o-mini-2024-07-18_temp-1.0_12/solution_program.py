import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money
    
    if spin_result % 2 == 0:  # Even number
        if 'even' in bets:
            total_money += bets['even']  # Player wins double on even
        if 'odd' in bets:
            total_money -= bets['odd']  # Player loses bet on odd
    else:  # Odd number
        if 'odd' in bets:
            total_money += bets['odd']  # Player wins double on odd
        if 'even' in bets:
            total_money -= bets['even']  # Player loses bet on even
    
    return total_money