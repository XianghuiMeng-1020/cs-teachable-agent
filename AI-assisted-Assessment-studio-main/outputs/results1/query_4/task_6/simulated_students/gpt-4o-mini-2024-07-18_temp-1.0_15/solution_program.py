import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    final_money = money
    
    if spin_result % 2 == 0:  # Even number
        if 'even' in bets:
            final_money += bets['even']  # Win even bet
        if 'odd' in bets:
            final_money -= bets['odd']  # Lose odd bet
    else:  # Odd number
        if 'odd' in bets:
            final_money += bets['odd']  # Win odd bet
        if 'even' in bets:
            final_money -= bets['even']  # Lose even bet
    
    return final_money