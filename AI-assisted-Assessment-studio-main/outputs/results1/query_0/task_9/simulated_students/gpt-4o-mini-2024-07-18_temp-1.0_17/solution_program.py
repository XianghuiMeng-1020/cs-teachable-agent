import random

with open('player_choice.txt', 'r') as file:
    player_choice = file.readline().strip()

player_number = int(player_choice)
random_number = random.randint(1, 10)

with open('outcome.txt', 'w') as outcome_file:
    if player_number == random_number:
        outcome_file.write(f'Congratulations! You won! Lucky number: {random_number}')
    else:
        outcome_file.write(f'Sorry! Better luck next time. Chosen number: {player_number}, Generated number: {random_number}')