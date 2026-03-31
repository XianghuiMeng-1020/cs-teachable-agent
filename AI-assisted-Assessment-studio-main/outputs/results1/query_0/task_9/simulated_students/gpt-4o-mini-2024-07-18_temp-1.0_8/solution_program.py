import random

# Read player's choice from file
with open('player_choice.txt', 'r') as file:
    player_choice = int(file.readline().strip())

# Generate a random number between 1 and 10
random_number = random.randint(1, 10)

# Compare and write outcome to file
with open('outcome.txt', 'w') as file:
    if player_choice == random_number:
        file.write(f'Congratulations! You won! Lucky number: {random_number}')
    else:
        file.write(f'Sorry! Better luck next time. Chosen number: {player_choice}, Generated number: {random_number}')