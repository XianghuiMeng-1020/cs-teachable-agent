def play_lucky_guess(input_file, output_file):
    with open('secret_number.txt', 'r') as secret_file:
        secret_number = int(secret_file.read().strip())

    with open(input_file, 'r') as guesses_file:
        guesses = guesses_file.readlines()

    with open(output_file, 'w') as results_file:
        for guess in guesses:
            guess_number = int(guess.strip())
            if guess_number < secret_number:
                results_file.write('too low\n')
            elif guess_number > secret_number:
                results_file.write('too high\n')
            else:
                results_file.write('correct\n')
                break
