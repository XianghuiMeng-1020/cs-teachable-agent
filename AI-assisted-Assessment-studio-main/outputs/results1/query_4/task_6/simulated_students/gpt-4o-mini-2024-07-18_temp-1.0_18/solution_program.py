import random

def roulette_game(money, bets):
    spin_result = random.randint(1, 36)
    total_money = money
    
    if spin_result % 2 == 0:
        result_type = 'even'
    else:
        result_type = 'odd'
    
    for bet_type, bet_amount in bets.items():
        if bet_type in ['even', 'odd'] and bet_amount > 0:
            if bet_amount <= total_money:
                if bet_type == result_type:
                    total_money += bet_amount  # player wins, get double their bet
                else:
                    total_money -= bet_amount  # player loses their bet
    
    return total_money