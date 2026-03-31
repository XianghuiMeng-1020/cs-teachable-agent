def lottery_stub_generator(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

    results = []
    for line in lines:
        name, chosen_number, age = line.strip().split(',')
        chosen_number = int(chosen_number)
        age = int(age)
        winning_condition = ((chosen_number + age) * 2) % 5 == 0
        result = "WIN" if winning_condition else "LOSE"
        results.append(f"{name},{chosen_number},{age},{result}")

    with open(output_file, 'w') as outfile:
        for result in results:
            outfile.write(result + '\n')