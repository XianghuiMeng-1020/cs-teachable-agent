import random

file_path = 'player_choice.txt'

with open(file_path, 'r') as file:
    player_choice = int(file.readline().strip())

generated_number = random.randint(1, 10)

if player_choice == generated_number:
    outcome_message = f'Congratulations! You won! Lucky number: {generated_number}'
else:
    outcome_message = f'Sorry! Better luck next time. Chosen number: {player_choice}, Generated number: {generated_number}'

with open('outcome.txt', 'w') as outcome_file:
    outcome_file.write(outcome_message)