def count_creatures(input_file, output_file):
    creature_count = {}
    with open(input_file, 'r') as file:
        for line in file:
            # Split the line into creature name and category
            _, category = line.strip().split(' - ')
            # Count occurrences of each category
            if category in creature_count:
                creature_count[category] += 1
            else:
                creature_count[category] = 1

    with open(output_file, 'w') as file:
        for category, count in creature_count.items():
            file.write(f'{category}: {count}\n')