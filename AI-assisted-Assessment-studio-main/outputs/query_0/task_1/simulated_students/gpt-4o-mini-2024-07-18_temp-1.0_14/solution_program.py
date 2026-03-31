def generate_lucky_numbers(input_file, output_file):
    with open(input_file, 'r') as file:
        names = file.readlines()

    lucky_numbers = []
    for name in names:
        name = name.strip()
        length = len(name)
        if length % 2 == 0:
            lucky_number = length * 3
        else:
            lucky_number = length * 5 - 2
        lucky_numbers.append(f'{name}: {lucky_number}')

    with open(output_file, 'w') as file:
        for entry in lucky_numbers:
            file.write(entry + '\n')