def count_creatures(input_file, output_file):
    creature_counts = {}
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) == 2:
                creature_name, category = parts
                if category in creature_counts:
                    creature_counts[category] += 1
                else:
                    creature_counts[category] = 1
    with open(output_file, 'w') as file:
        for category, count in creature_counts.items():
            file.write(f'{category}: {count}\n')