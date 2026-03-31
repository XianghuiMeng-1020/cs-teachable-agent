def play_lucky_guess(input_file, output_file):
    with open('secret_number.txt', 'r') as sn_file:
        secret_number = int(sn_file.read().strip())

    with open(input_file, 'r') as in_file:
        guesses = [int(line.strip()) for line in in_file.readlines()]

    with open(output_file, 'w') as out_file:
        for guess in guesses:
            if guess < secret_number:
                out_file.write('too low\n')
            elif guess > secret_number:
                out_file.write('too high\n')
            else:
                out_file.write('correct\n')
                break
