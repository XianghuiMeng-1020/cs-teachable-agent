def calculate_gravitational_force(input_filepath, output_filepath):
    G = 6.67430e-11
    with open(input_filepath, 'r') as infile, open(output_filepath, 'w') as outfile:
        for line in infile:
            mass1, distance, mass2 = map(float, line.strip().split(','))
            force = (G * mass1 * mass2) / (distance ** 2)
            outfile.write(f'{force:.2f}\n')