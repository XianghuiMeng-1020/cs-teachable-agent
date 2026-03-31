def determine_ultimate_being(input_file_path):
    creatures = {}
    with open(input_file_path, 'r') as f:
        for line in f:
            name, power = line.strip().split(';')
            creatures[name] = int(power)

    max_power = max(creatures.values())
    strong_creatures = [name for name, power in creatures.items() if power == max_power]

    with open('ultimate_being.txt', 'w') as f:
        if len(strong_creatures) > 1:
            f.write("It's a draw")
        else:
            f.write(strong_creatures[0])