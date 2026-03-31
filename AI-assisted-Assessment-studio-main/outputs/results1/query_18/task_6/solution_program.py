def calculate_gravitational_force(input_filepath, output_filepath):
    G = 6.67430e-11
    with open(input_filepath, 'r') as infile:
        data_lines = infile.readlines()
    results = []
    for line in data_lines:
        mass1, distance, mass2 = map(float, line.strip().split(','))
        force = (G * mass1 * mass2) / (distance ** 2)
        results.append(f"{force:.2f}\n")
    with open(output_filepath, 'w') as outfile:
        outfile.writelines(results)
