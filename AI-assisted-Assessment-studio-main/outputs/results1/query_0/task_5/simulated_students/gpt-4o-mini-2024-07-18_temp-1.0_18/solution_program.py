import random

def play_game_of_chance():
    with open('words.txt', 'r') as file:
        words = [line.strip() for line in file]  # Read words from the file
    selected_word = random.choice(words)  # Randomly select a word

    guess = input('Enter your guess: ').strip()  # Get guess from user
    result = ''

    if guess == selected_word:
        result = "Correct! You've won!"
        outcome = 'won'
    else:
        result = "Incorrect! Try again another time!"
        outcome = 'lost'

    print(result)  # Output the game result

    with open('game_results.txt', 'a') as results_file:
        results_file.write(f'{guess} - {outcome}\n')  # Record the result