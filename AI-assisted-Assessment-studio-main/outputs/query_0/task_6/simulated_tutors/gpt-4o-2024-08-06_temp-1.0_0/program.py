import os

def play_lucky_guess(input_file, output_file):
    # Read the secret number from 'secret_number.txt'
    with open('secret_number.txt', 'r') as f:
        secret_number = int(f.read().strip())

    # Prepare to read input guesses and write output results
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            try:
                guess = int(line.strip())
                if guess < secret_number:
                    outfile.write("too low\n")
                elif guess > secret_number:
                    outfile.write("too high\n")
                else:
                    outfile.write("correct\n")
                    break
            except ValueError:
                continue
