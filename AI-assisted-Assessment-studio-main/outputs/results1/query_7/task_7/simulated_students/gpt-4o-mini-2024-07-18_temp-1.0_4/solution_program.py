def count_creatures(input_file, output_file):
    category_count = {}
    with open(input_file, 'r') as f:
        for line in f:
            _, category = line.strip().split(' - ')
            if category in category_count:
                category_count[category] += 1
            else:
                category_count[category] = 1
    with open(output_file, 'w') as f:
        for category, count in category_count.items():
            f.write(f'{category}: {count}\n')