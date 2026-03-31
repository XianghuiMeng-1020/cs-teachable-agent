def calculate_points(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            string = line.strip()
            points = 0
            points += string.count('a')
            points += string.count('xyz') * 3
            if len(string) == 7:
                points += 5
            outfile.write(f'{points}\n')