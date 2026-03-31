def play_lucky_guess(input_file, output_file):
    with open('secret_number.txt', 'r') as secret_file:
        secret_number = int(secret_file.read().strip())

    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            guess = int(line.strip())
            if guess < secret_number:
                outfile.write('too low\n')
            elif guess > secret_number:
                outfile.write('too high\n')
            else:
                outfile.write('correct\n')
                break
