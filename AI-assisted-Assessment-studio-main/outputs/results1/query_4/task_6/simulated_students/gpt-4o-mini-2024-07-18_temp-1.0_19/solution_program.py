import random

def roulette_game(money, bets):
    winning_number = random.randint(1, 36)
    even_win = winning_number % 2 == 0
    total_money = money

    for bet_type, bet_amount in bets.items():
        if bet_type == "even" and even_win:
            total_money += bet_amount   # win, receive double the bet
        elif bet_type == "odd" and not even_win:
            total_money += bet_amount   # win, receive double the bet
        total_money -= bet_amount       # lose, subtract the bet amount

    return total_money