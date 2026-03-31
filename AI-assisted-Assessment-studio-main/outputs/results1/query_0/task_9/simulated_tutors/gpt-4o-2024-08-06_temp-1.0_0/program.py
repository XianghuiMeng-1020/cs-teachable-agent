import random

def lucky_draw():
    # Read the player's chosen number from the file
    with open('player_choice.txt', 'r') as file:
        player_choice = int(file.readline().strip())

    # Generate a random number between 1 and 10
    generated_number = random.randint(1, 10)

    # Compare the numbers and write the outcome to the file
    with open('outcome.txt', 'w') as file:
        if player_choice == generated_number:
            file.write(f'Congratulations! You won! Lucky number: {generated_number}')
        else:
            file.write(f'Sorry! Better luck next time. Chosen number: {player_choice}, Generated number: {generated_number}')