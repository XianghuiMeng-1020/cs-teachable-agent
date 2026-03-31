def play_lucky_guess(input_file, output_file):
    with open('secret_number.txt', 'r') as f:
        secret_number = int(f.read().strip())

    with open(input_file, 'r') as f:
        guesses = [int(line.strip()) for line in f.readlines()]

    results = []
    for guess in guesses:
        if guess < secret_number:
            results.append('too low')
        elif guess > secret_number:
            results.append('too high')
        else:
            results.append('correct')
            break

    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + '\n')