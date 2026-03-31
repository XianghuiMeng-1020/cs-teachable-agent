def calculate_points(input_file, output_file):
    with open(input_file, 'r') as file:
        strings = file.readlines()
    results = []
    for string in strings:
        string = string.strip()
        points = 0
        if 'xyz' in string:
            points += 3
        points += string.count('a')
        if len(string) == 7:
            points += 5
        results.append(str(points))
    with open(output_file, 'w') as file:
        file.write('\n'.join(results))