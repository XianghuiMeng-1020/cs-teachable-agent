import random

# Read player's chosen number from the file
with open('player_choice.txt', 'r') as file:
    player_choice = int(file.readline().strip())

# Generate a random number between 1 and 10
random_number = random.randint(1, 10)

# Prepare the outcome message
if player_choice == random_number:
    message = f'Congratulations! You won! Lucky number: {random_number}'
else:
    message = f'Sorry! Better luck next time. Chosen number: {player_choice}, Generated number: {random_number}'

# Write the outcome message to the file
with open('outcome.txt', 'w') as file:
    file.write(message)