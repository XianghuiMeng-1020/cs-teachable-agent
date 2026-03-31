def calculate_points(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            points = 0
            if 'xyz' in line:
                points += 3
            points += line.count('a')
            if len(line) == 7:
                points += 5
            outfile.write(str(points) + '\n')