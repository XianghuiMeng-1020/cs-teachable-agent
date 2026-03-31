def count_creatures(input_file, output_file):
    creature_counts = {}
    
    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.strip()  # Remove any trailing newline characters
            if '-' in line:
                category = line.split('-')[1].strip()  # Get the category part
                if category in creature_counts:
                    creature_counts[category] += 1
                else:
                    creature_counts[category] = 1
    
    with open(output_file, 'w') as outfile:
        for category, count in creature_counts.items():
            outfile.write(f'{category}: {count}\n')