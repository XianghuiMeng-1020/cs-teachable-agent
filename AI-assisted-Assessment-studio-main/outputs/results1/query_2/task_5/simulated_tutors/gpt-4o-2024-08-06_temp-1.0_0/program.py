def calculate_points(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()  # Remove any surrounding whitespace
            points = 0
            
            # Rule 1: Check if 'xyz' is in the string
            if 'xyz' in line:
                points += 3

            # Rule 2: Count the 'a' characters
            points += line.count('a')

            # Rule 3: Check string length
            if len(line) == 7:
                points += 5

            # Write the total points to the output file
            outfile.write(str(points) + '\n')