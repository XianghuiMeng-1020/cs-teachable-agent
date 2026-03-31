import random

def play_game_of_chance():
    with open('words.txt', 'r') as file:
        words = [word.strip() for word in file.readlines()]

    selected_word = random.choice(words)
    guess = input('Please enter your guess: ')

    if guess == selected_word:
        result = "Correct! You've won!"
        outcome = 'won'
    else:
        result = "Incorrect! Try again another time!"
        outcome = 'lost'

    print(result)

    with open('game_results.txt', 'a') as results_file:
        results_file.write(f'{guess} {outcome}\n')