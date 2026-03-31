def lottery_stub_generator(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            name, chosen_number, age = line.strip().split(',')
            chosen_number = int(chosen_number)
            age = int(age)
            if ((chosen_number + age) * 2) % 5 == 0:
                result = 'WIN'
            else:
                result = 'LOSE'
            outfile.write(f'{name},{chosen_number},{age},{result}\n')