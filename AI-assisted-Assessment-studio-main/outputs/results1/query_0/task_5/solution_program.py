import random

def play_game_of_chance():
    with open('words.txt', 'r') as file:
        words = file.read().splitlines()
    random_word = random.choice(words)
    guess = input("Guess the word: ").strip()
    result = 'won' if guess == random_word else 'lost'
    if result == 'won':
        print("Correct! You've won!")
    else:
        print("Incorrect! Try again another time!")
    with open('game_results.txt', 'a') as file:
        file.write(f"{guess} {result}\n")