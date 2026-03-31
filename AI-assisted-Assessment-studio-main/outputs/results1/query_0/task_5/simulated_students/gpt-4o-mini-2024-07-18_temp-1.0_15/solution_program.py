import random


def play_game_of_chance():
    with open('words.txt', 'r') as file:
        words = [line.strip() for line in file.readlines()]

    selected_word = random.choice(words)
    player_guess = input('Please enter your guess: ').strip()

    if player_guess == selected_word:
        result = "Correct! You've won!"
        outcome = "won"
    else:
        result = "Incorrect! Try again another time!"
        outcome = "lost"

    print(result)

    with open('game_results.txt', 'a') as results_file:
        results_file.write(f'{player_guess} - {outcome}\n')