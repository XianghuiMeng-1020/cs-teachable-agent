def calculate_points(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            string = line.strip()
            points = 0
            
            if 'xyz' in string:
                points += 3
            points += string.count('a')
            
            if len(string) == 7:
                points += 5
            
            outfile.write(str(points) + '\n')