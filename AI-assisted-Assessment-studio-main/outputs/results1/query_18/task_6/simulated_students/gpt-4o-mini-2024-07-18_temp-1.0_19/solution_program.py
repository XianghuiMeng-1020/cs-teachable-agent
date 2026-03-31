def calculate_gravitational_force(input_filepath, output_filepath):
    G = 6.67430e-11
    with open(input_filepath, 'r') as infile:
        data = infile.readlines()
    results = []
    for line in data:
        mass1, distance, mass2 = map(float, line.split(','))
        F = (G * mass1 * mass2) / (distance ** 2)
        results.append(f'{F:.2f}')
    with open(output_filepath, 'w') as outfile:
        outfile.write('\n'.join(results) + '\n')