def analyse_dice_game(input_file, output_file):
    # Initialize counters for wins, loses, and draws
    wins = 0
    loses = 0
    draws = 0

    # Open the input file and process each line
    with open(input_file, 'r') as file:
        for line in file:
            outcome = line.strip()
            if outcome == "win":
                wins += 1
            elif outcome == "lose":
                loses += 1
            elif outcome == "draw":
                draws += 1

    # Prepare the output text
    result = f"Wins: {wins}\nLoses: {loses}\nDraws: {draws}\n"

    # Write the result to the output file
    with open(output_file, 'w') as file:
        file.write(result)
