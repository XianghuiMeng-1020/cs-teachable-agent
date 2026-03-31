def count_creatures(input_file, output_file):
    category_count = {}
    with open(input_file, 'r') as file:
        for line in file:
            _, category = line.strip().split(' - ')
            if category in category_count:
                category_count[category] += 1
            else:
                category_count[category] = 1
    with open(output_file, 'w') as outfile:
        for category, count in category_count.items():
            outfile.write(f'{category}: {count}\n')