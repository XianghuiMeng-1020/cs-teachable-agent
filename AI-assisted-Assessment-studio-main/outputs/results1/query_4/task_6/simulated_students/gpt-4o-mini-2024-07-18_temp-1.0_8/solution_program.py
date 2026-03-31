import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    if spin_result % 2 == 0:
        outcome = "even"
    else:
        outcome = "odd"

    total_money = money
    for bet, amount in bets.items():
        if amount > 0:
            if bet == outcome:
                total_money += amount
            else:
                total_money -= amount

    return total_money