import random

# Step 1: Read the player's choice from the file
with open('player_choice.txt', 'r') as file:
    player_choice = int(file.readline().strip())

# Step 2: Generate a random number between 1 and 10
random_number = random.randint(1, 10)

# Step 3: Determine the outcome and write it to the outcome file
if player_choice == random_number:
    outcome_message = f'Congratulations! You won! Lucky number: {random_number}'
else:
    outcome_message = f'Sorry! Better luck next time. Chosen number: {player_choice}, Generated number: {random_number}'

with open('outcome.txt', 'w') as outcome_file:
    outcome_file.write(outcome_message)