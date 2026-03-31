import random

with open('player_choice.txt', 'r') as file:
    player_choice = int(file.readline().strip())

random_number = random.randint(1, 10)

if player_choice == random_number:
    outcome = f'Congratulations! You won! Lucky number: {random_number}'
else:
    outcome = f'Sorry! Better luck next time. Chosen number: {player_choice}, Generated number: {random_number}'

with open('outcome.txt', 'w') as file:
    file.write(outcome)