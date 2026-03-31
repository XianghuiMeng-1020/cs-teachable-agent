def determine_ultimate_being(input_file_path):
    with open(input_file_path, 'r') as infile:
        lines = infile.readlines()

    max_power = -1
    ultimate_creature = ""
    is_draw = False

    for line in lines:
        name, power_str = line.strip().split(';')
        power = int(power_str)

        if power > max_power:
            max_power = power
            ultimate_creature = name
            is_draw = False
        elif power == max_power:
            is_draw = True

    with open('ultimate_being.txt', 'w') as outfile:
        if is_draw:
            outfile.write("It's a draw")
        else:
            outfile.write(ultimate_creature)