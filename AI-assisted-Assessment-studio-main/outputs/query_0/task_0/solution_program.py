def lottery_stub_generator(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        for line in lines:
            parts = line.strip().split(',')
            if len(parts) != 3:
                continue
            name, number, age = parts
            number = int(number)
            age = int(age)
            result = 'WIN' if ((number + age) * 2) % 5 == 0 else 'LOSE'
            outfile.write(f'{name},{number},{age},{result}\n')