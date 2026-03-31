def play_lucky_guess(input_file, output_file):
    with open('secret_number.txt', 'r') as sn_file:
        secret_number = int(sn_file.read().strip())

    with open(input_file, 'r') as guess_file:
        guesses = guess_file.readlines()

    results = []
    for guess in guesses:
        guess = int(guess.strip())
        if guess < secret_number:
            results.append('too low')
        elif guess > secret_number:
            results.append('too high')
        else:
            results.append('correct')
            break

    with open(output_file, 'w') as result_file:
        for result in results:
            result_file.write(result + '\n')