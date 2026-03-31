import random

def play_game_of_chance():
    # Read words from file
    with open('words.txt', 'r') as file:
        words = [line.strip() for line in file]
    
    # Randomly select a word
    selected_word = random.choice(words)

    # Get user guess
    guess = input("Guess the word: ")

    # Determine if guess is correct
    if guess == selected_word:
        print("Correct! You've won!")
        result = "won"
    else:
        print("Incorrect! Try again another time!")
        result = "lost"

    # Write the result to file
    with open('game_results.txt', 'a') as file:
        file.write(f"{guess} {result}\n")