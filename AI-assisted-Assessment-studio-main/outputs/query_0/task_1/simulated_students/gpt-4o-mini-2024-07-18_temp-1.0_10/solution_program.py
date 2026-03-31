def generate_lucky_numbers(input_file, output_file):
    with open(input_file, 'r') as infile:
        names = infile.readlines()

    lucky_numbers = []
    for name in names:
        name = name.strip()
        length = len(name)
        if length % 2 == 0:
            lucky_number = length * 3
        else:
            lucky_number = length * 5 - 2
        lucky_numbers.append(f'{name}: {lucky_number}')

    with open(output_file, 'w') as outfile:
        for line in lucky_numbers:
            outfile.write(line + '\n')