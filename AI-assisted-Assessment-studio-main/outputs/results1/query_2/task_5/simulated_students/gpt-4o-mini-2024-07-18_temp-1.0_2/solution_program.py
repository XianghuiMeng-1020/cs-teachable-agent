def calculate_points(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()  
    results = []
    for line in lines:
        string = line.strip()
        points = 0
        if 'xyz' in string:
            points += 3 * string.count('xyz')
        points += string.count('a')
        if len(string) == 7:
            points += 5
        results.append(str(points))
    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(results) + '\n')