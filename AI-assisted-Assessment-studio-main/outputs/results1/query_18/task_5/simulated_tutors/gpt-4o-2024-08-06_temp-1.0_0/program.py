def calculate_final_weight(filename):
    # Define the initial weight
    initial_weight = 1000
    final_weight = initial_weight

    # Open the file to read weight changes
    with open(filename, 'r') as file:
        # Read each line in the file and update the weight
        for line in file:
            change = int(line.strip())
            final_weight += change

    # Write the final weight to the output file
    with open('final_weight.txt', 'w') as file:
        file.write(f"{final_weight}\n")