def determine_ultimate_being(input_file_path):
    creatures = {}
    with open(input_file_path, 'r') as file:
        for line in file:
            name, power = line.strip().split(';')
            creatures[name] = int(power)

    max_power = max(creatures.values())
    ultimate_beings = [name for name, power in creatures.items() if power == max_power]

    with open('ultimate_being.txt', 'w') as output_file:
        if len(ultimate_beings) > 1:
            output_file.write("It's a draw")
        else:
            output_file.write(ultimate_beings[0])