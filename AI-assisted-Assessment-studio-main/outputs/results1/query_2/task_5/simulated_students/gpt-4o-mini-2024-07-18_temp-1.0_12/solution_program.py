def calculate_points(input_file, output_file):
    with open(input_file, 'r') as infile:
        strings = infile.readlines()
    points = []
    for s in strings:
        s = s.strip()
        score = 0
        score += s.count('xyz') * 3
        score += s.count('a') * 1
        if len(s) == 7:
            score += 5
        points.append(str(score))
    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(points) + '\n')