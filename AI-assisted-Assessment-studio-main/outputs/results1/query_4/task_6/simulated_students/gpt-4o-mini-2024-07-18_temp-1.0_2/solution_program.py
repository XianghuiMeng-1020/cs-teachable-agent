import random

def roulette_game(money, bets):
    # Spin the roulette wheel to get a number between 1 and 36
    spin_result = random.randint(1, 36)
    total_money = money

    # Check if the player has placed bets
    if bets:
        # Process the bets on 'even' and 'odd'
        if 'even' in bets:
            if spin_result % 2 == 0:  # Win condition for even
                total_money += bets['even']  # Double the bet
            else:  # Lose condition for even
                total_money -= bets['even']
        if 'odd' in bets:
            if spin_result % 2 != 0:  # Win condition for odd
                total_money += bets['odd']  # Double the bet
            else:  # Lose condition for odd
                total_money -= bets['odd']

    return total_money