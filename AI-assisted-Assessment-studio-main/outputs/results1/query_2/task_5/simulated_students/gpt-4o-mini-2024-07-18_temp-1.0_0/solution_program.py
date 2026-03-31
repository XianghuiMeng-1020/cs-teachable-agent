def calculate_points(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    results = []
    for line in lines:
        line = line.strip()
        points = 0

        if 'xyz' in line:
            points += 3 * line.count('xyz')
        points += line.count('a')

        if len(line) == 7:
            points += 5

        results.append(str(points))

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(results) + '\n')