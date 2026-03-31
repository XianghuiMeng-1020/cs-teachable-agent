import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money

    if spin_result % 2 == 0:
        result = "even"
    else:
        result = "odd"

    for bet_type, bet_amount in bets.items():
        if bet_type == "even" and result == "even":
            total_money += bet_amount  # Winning double the bet amount
        elif bet_type == "even":
            total_money -= bet_amount  # Losing the bet amount
        elif bet_type == "odd" and result == "odd":
            total_money += bet_amount  # Winning double the bet amount
        elif bet_type == "odd":
            total_money -= bet_amount  # Losing the bet amount

    return total_money