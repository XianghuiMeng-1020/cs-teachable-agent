def calculate_points(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            string = line.strip()
            points = 0
            # Rule 1: Check for 'xyz'
            points += string.count('xyz') * 3
            # Rule 2: Count instances of 'a'
            points += string.count('a')
            # Rule 3: Check if length is 7
            if len(string) == 7:
                points += 5
            outfile.write(str(points) + '\n')