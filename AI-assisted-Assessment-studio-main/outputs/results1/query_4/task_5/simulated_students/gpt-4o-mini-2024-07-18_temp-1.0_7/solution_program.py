import random

def play_roulette(starting_amount, rounds, bets):
    remaining_amount = starting_amount
    played_rounds = 0

    for i in range(rounds):
        color, amount = bets[i]
        if remaining_amount == 0:
            break
        
        if amount > remaining_amount:
            continue  # Skip the bet if it exceeds remaining funds

        result = random.randint(0, 1)
        if (result == 0 and color == 'red') or (result == 1 and color == 'black'):
            remaining_amount += amount  # Win
        else:
            remaining_amount -= amount  # Lose
        
        played_rounds += 1

    return {'remaining_amount': remaining_amount, 'played_rounds': played_rounds}