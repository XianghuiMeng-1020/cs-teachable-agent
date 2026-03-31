def count_creatures(input_file, output_file):
    creature_counts = {}
    with open(input_file, 'r') as file:
        for line in file:
            _, category = line.strip().split(' - ')
            if category in creature_counts:
                creature_counts[category] += 1
            else:
                creature_counts[category] = 1
    with open(output_file, 'w') as file:
        for category, count in creature_counts.items():
            file.write(f'{category}: {count}\n')