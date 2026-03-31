def count_creatures(input_file, output_file):
    with open(input_file, 'r') as f:
        creature_data = f.readlines()
    
    category_count = {}
    for line in creature_data:
        if '-' in line:
            _, category = line.split('-', 1)
            category = category.strip()
            if category in category_count:
                category_count[category] += 1
            else:
                category_count[category] = 1

    with open(output_file, 'w') as f:
        for category, count in category_count.items():
            f.write(f'{category}: {count}\n')