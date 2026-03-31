import random

def play_game_of_chance():
    # Read words from the file
    with open('words.txt', 'r') as file:
        words = [line.strip() for line in file.readlines()]

    # Randomly select a word
    selected_word = random.choice(words)
    
    # Get player's guess
    player_guess = input('Enter your guess: ').strip()
    
    # Determine if the guess is correct
    if player_guess == selected_word:
        result = "Correct! You've won!"
        outcome = 'won'
    else:
        result = "Incorrect! Try again another time!"
        outcome = 'lost'
    
    # Display the result
    print(result)
    
    # Record the result in the game_results.txt file
    with open('game_results.txt', 'a') as results_file:
        results_file.write(f'{player_guess} - {outcome}\n')