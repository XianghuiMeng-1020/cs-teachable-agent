def generate_lucky_numbers(input_file, output_file):
    with open(input_file, 'r') as file:
        names = file.readlines()
    results = []
    for name in names:
        name = name.strip()
        name_length = len(name)
        if name_length % 2 == 0:
            lucky_number = name_length * 3
        else:
            lucky_number = name_length * 5 - 2
        results.append(f'{name}: {lucky_number}')
    with open(output_file, 'w') as file:
        for result in results:
            file.write(result + '\n')