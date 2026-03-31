import random

# Read the player's choice from a file
with open('player_choice.txt', 'r') as f:
    player_choice = int(f.readline().strip())

# Generate a random number between 1 and 10
generated_number = random.randint(1, 10)

# Determine the outcome and write to the outcome file
if player_choice == generated_number:
    outcome_message = f'Congratulations! You won! Lucky number: {generated_number}'
else:
    outcome_message = f'Sorry! Better luck next time. Chosen number: {player_choice}, Generated number: {generated_number}'

with open('outcome.txt', 'w') as f:
    f.write(outcome_message)