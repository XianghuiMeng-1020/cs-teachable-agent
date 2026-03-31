def determine_ultimate_being(input_file_path):
    # Read the input file and extract creatures and their powers
    creatures = {}
    with open(input_file_path, 'r') as file:
        for line in file:
            name, power = line.strip().split(';')
            creatures[name] = int(power)

    # Determine the creature(s) with the highest power
    max_power = max(creatures.values())
    ultimate_beings = [name for name, power in creatures.items() if power == max_power]

    # Write the result to the output file
    with open('ultimate_being.txt', 'w') as output_file:
        if len(ultimate_beings) > 1:
            output_file.write("It's a draw")
        else:
            output_file.write(ultimate_beings[0])