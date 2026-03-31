def generate_lucky_numbers(input_file, output_file):
    try:
        with open(input_file, 'r') as infile:
            names = infile.readlines()
        lucky_numbers = []
        for name in names:
            name = name.strip()  # Remove any trailing newline characters
            length = len(name)
            if length % 2 == 0:  # Even length
                lucky_number = length * 3
            else:  # Odd length
                lucky_number = length * 5 - 2
            lucky_numbers.append(f"{name}: {lucky_number}")
        with open(output_file, 'w') as outfile:
            for item in lucky_numbers:
                outfile.write(item + "\n")
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")