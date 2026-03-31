def calculate_points(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            s = line.strip()
            points = 0
            
            if 'xyz' in s:
                points += 3
            
            points += s.count('a')
            
            if len(s) == 7:
                points += 5
            
            outfile.write(str(points) + '\n')