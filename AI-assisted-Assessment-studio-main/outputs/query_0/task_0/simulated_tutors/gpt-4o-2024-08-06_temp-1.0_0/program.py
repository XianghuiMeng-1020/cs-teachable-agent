def lottery_stub_generator(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue

            parts = line.split(',')
            if len(parts) != 3:
                continue

            name, chosen_number, age = parts
            try:
                chosen_number = int(chosen_number)
                age = int(age)
            except ValueError:
                continue

            total = (chosen_number + age) * 2
            result = "WIN" if total % 5 == 0 else "LOSE"
            
            outfile.write(f"{name},{chosen_number},{age},{result}\n")