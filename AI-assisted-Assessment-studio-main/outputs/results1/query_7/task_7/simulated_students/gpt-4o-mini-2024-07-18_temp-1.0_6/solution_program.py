def count_creatures(input_file, output_file):
    category_counts = {}
    with open(input_file, 'r') as file:
        for line in file:
            creature_info = line.strip().split(' - ')
            if len(creature_info) == 2:
                category = creature_info[1].strip()
                if category in category_counts:
                    category_counts[category] += 1
                else:
                    category_counts[category] = 1
    with open(output_file, 'w') as file:
        for category, count in category_counts.items():
            file.write(f'{category}: {count}\n')
