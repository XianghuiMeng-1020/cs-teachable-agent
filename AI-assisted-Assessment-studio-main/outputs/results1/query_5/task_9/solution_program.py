def determine_ultimate_being(input_file_path):
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    highest_power = None
    ultimate_being = None
    draw = False

    for line in lines:
        creature, power = line.strip().split(';')
        power = int(power)
        
        if highest_power is None or power > highest_power:
            highest_power = power
            ultimate_being = creature
            draw = False
        elif power == highest_power:
            draw = True

    with open('ultimate_being.txt', 'w') as output_file:
        if draw:
            output_file.write("It's a draw")
        else:
            output_file.write(ultimate_being)