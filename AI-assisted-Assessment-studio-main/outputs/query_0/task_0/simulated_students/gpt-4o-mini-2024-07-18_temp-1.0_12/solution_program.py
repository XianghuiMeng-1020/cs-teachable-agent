def lottery_stub_generator(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            name, chosen_number_str, age_str = line.strip().split(',')
            chosen_number = int(chosen_number_str)
            age = int(age_str)
            result = 'WIN' if ((chosen_number + age) * 2) % 5 == 0 else 'LOSE'
            outfile.write(f'{name},{chosen_number},{age},{result}\n')