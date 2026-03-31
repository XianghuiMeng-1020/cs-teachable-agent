import random

# Read player's choice from the text file
with open('player_choice.txt', 'r') as file:
    player_choice = int(file.readline().strip())

# Generate a random number between 1 and 10
random_number = random.randint(1, 10)

# Determine the outcome
if player_choice == random_number:
    outcome_message = f'Congratulations! You won! Lucky number: {random_number}'
else:
    outcome_message = f'Sorry! Better luck next time. Chosen number: {player_choice}, Generated number: {random_number}'

# Write the outcome to the outcome.txt file
with open('outcome.txt', 'w') as file:
    file.write(outcome_message)