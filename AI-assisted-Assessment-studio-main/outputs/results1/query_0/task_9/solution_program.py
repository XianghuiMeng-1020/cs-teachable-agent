import random

def lucky_draw():
    with open('player_choice.txt', 'r') as f:
        chosen_number = int(f.readline().strip())
    random_number = random.randint(1, 10)
    if chosen_number == random_number:
        outcome = f'Congratulations! You won! Lucky number: {random_number}'
    else:
        outcome = f'Sorry! Better luck next time. Chosen number: {chosen_number}, Generated number: {random_number}'
    with open('outcome.txt', 'w') as f:
        f.write(outcome)