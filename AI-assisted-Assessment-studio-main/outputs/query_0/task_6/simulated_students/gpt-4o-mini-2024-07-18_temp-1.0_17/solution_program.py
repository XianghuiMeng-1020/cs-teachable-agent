def play_lucky_guess(input_file, output_file):
    with open('secret_number.txt', 'r') as sn_file:
        secret_number = int(sn_file.read().strip())

    with open(input_file, 'r') as guesses_file:
        guesses = [int(line.strip()) for line in guesses_file.readlines()]

    results = []
    for guess in guesses:
        if guess < secret_number:
            results.append('too low')
        elif guess > secret_number:
            results.append('too high')
        else:
            results.append('correct')
            break

    with open(output_file, 'w') as results_file:
        results_file.write('\n'.join(results))