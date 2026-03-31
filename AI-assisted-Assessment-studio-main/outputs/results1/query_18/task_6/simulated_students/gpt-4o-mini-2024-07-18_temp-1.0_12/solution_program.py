def calculate_gravitational_force(input_filepath, output_filepath):
    G = 6.67430e-11
    with open(input_filepath, 'r') as infile:
        lines = infile.readlines()
    forces = []
    for line in lines:
        mass1, distance, mass2 = map(float, line.strip().split(','))
        force = (G * mass1 * mass2) / (distance ** 2)
        forces.append(f'{force:.2f}')
    with open(output_filepath, 'w') as outfile:
        outfile.write('\n'.join(forces) + '\n')