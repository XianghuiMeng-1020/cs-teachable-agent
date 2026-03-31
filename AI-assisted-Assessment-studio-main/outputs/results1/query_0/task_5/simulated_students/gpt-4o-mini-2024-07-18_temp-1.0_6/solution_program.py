import random

def play_game_of_chance():
    with open('words.txt', 'r') as file:
        words = [line.strip() for line in file.readlines()]
    selected_word = random.choice(words)
    guess = input('Enter your guess: ')  
    if guess == selected_word:
        result = "Correct! You've won!"
        outcome = "won"
    else:
        result = "Incorrect! Try again another time!"
        outcome = "lost"
    with open('game_results.txt', 'a') as result_file:
        result_file.write(f'{guess} {outcome}\n')
    print(result)