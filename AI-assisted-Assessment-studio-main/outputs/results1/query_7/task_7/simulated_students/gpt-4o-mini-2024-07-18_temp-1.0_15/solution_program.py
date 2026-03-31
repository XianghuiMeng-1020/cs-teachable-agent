def count_creatures(input_file, output_file):
    category_counts = {}
    with open(input_file, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) > 1:
                category = parts[1]
                if category in category_counts:
                    category_counts[category] += 1
                else:
                    category_counts[category] = 1
    with open(output_file, 'w') as file:
        for category, count in category_counts.items():
            file.write(f'{category}: {count}\n')