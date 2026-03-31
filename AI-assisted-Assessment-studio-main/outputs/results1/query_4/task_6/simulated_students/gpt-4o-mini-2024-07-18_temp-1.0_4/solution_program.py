import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    winnings = money
    
    if spin_result % 2 == 0:  # Even number
        if 'even' in bets:
            winnings += bets['even']  # Winning on even
        if 'odd' in bets:
            winnings -= bets['odd']  # Losing on odd
    else:  # Odd number
        if 'odd' in bets:
            winnings += bets['odd']  # Winning on odd
        if 'even' in bets:
            winnings -= bets['even']  # Losing on even
    
    return winnings