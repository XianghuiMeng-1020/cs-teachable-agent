import random


def play_game_of_chance():
    with open('words.txt', 'r') as file:
        words = [line.strip() for line in file.readlines()]

    selected_word = random.choice(words)
    guess = input('Guess the word: ').strip()

    if guess == selected_word:
        result = 'won'
        print("Correct! You've won!")
    else:
        result = 'lost'
        print("Incorrect! Try again another time!")

    with open('game_results.txt', 'a') as results_file:
        results_file.write(f'{guess} {result}\n')