import random

def play_game_of_chance():
    with open('words.txt', 'r') as file:
        words = file.read().splitlines()
    selected_word = random.choice(words)
    player_guess = input('Please enter your guess: ')
    if player_guess == selected_word:
        print("Correct! You've won!")
        result = 'won'
    else:
        print("Incorrect! Try again another time!")
        result = 'lost'
    with open('game_results.txt', 'a') as results_file:
        results_file.write(f'{player_guess} {result}\n')