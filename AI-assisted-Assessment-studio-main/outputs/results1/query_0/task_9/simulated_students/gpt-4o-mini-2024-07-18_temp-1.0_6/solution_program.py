import random

with open('player_choice.txt', 'r') as file:
    player_choice = int(file.readline().strip())

generated_number = random.randint(1, 10)

if player_choice == generated_number:
    message = f'Congratulations! You won! Lucky number: {generated_number}'
else:
    message = f'Sorry! Better luck next time. Chosen number: {player_choice}, Generated number: {generated_number}'

with open('outcome.txt', 'w') as file:
    file.write(message)