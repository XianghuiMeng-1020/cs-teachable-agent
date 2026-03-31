def count_creatures(input_file, output_file):
    # Dictionary to hold the count of each category
    creature_count = {}
    
    # Open the input file and process each line
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()  # Remove trailing whitespace and newline characters
            if not line:
                continue  # Skip any empty lines
            
            name, category = line.split(' - ')  # Split on ' - '
            
            # Increment the count of the category
            if category in creature_count:
                creature_count[category] += 1
            else:
                creature_count[category] = 1

    # Write the results to the output file
    with open(output_file, 'w') as file:
        for category, count in creature_count.items():
            file.write(f"{category}: {count}\n")