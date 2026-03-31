import random

def play_game_of_chance():
    with open('words.txt', 'r') as f:
        word_list = [line.strip() for line in f.readlines()]

    selected_word = random.choice(word_list)
    guess = input('Guess the word: ').strip()

    if guess == selected_word:
        result = "Correct! You've won!"
        outcome = "won"
    else:
        result = "Incorrect! Try again another time!"
        outcome = "lost"

    print(result)

    with open('game_results.txt', 'a') as result_file:
        result_file.write(f'{guess} - {outcome}\n')