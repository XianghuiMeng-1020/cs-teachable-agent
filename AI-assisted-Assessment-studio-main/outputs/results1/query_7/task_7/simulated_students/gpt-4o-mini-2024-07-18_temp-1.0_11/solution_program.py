def count_creatures(input_file, output_file):
    category_count = {}

    with open(input_file, 'r') as infile:
        for line in infile:
            if '-' in line:
                _, category = line.split(' - ', 1)
                category = category.strip()
                if category not in category_count:
                    category_count[category] = 0
                category_count[category] += 1

    with open(output_file, 'w') as outfile:
        for category, count in category_count.items():
            outfile.write(f'{category}: {count}\n')