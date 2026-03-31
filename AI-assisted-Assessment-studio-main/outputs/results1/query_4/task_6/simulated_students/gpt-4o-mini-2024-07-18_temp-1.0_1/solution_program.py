import random

def roulette_game(money, bets):
    # Spin the roulette wheel, getting a random number between 1 and 36
    spin_result = random.randint(1, 36)  
    total_money = money

    # Check if the bets contain 'even' and process it
    if 'even' in bets:
        even_bet = bets['even']
        if spin_result % 2 == 0:
            total_money += even_bet  # Win: double the bet amount
        else:
            total_money -= even_bet  # Lose: lose the bet amount

    # Check if the bets contain 'odd' and process it
    if 'odd' in bets:
        odd_bet = bets['odd']
        if spin_result % 2 == 1:
            total_money += odd_bet  # Win: double the bet amount
        else:
            total_money -= odd_bet  # Lose: lose the bet amount

    return total_money