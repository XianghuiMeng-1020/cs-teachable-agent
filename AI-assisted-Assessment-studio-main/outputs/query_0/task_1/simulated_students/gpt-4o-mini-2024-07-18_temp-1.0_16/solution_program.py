def generate_lucky_numbers(input_file, output_file):
    with open(input_file, 'r') as infile:
        names = infile.read().strip().splitlines()

    results = []
    for name in names:
        length = len(name)
        if length % 2 == 0:
            lucky_number = length * 3
        else:
            lucky_number = length * 5 - 2
        results.append(f'{name}: {lucky_number}')

    with open(output_file, 'w') as outfile:
        outfile.write('\n'.join(results))