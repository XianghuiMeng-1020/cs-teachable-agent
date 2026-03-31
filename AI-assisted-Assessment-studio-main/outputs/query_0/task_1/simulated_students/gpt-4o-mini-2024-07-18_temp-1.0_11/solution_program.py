def generate_lucky_numbers(input_file, output_file):
    with open(input_file, 'r') as file:
        names = file.readlines()
    with open(output_file, 'w') as file:
        for name in names:
            name = name.strip()
            length = len(name)
            if length % 2 == 0:
                lucky_number = length * 3
            else:
                lucky_number = length * 5 - 2
            file.write(f'{name}: {lucky_number}\n')