def count_creatures(input_file, output_file):
    category_count = {}

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if ' - ' in line:
                _, category = line.split(' - ', 1)
                category = category.strip()
                if category in category_count:
                    category_count[category] += 1
                else:
                    category_count[category] = 1

    with open(output_file, 'w') as file:
        for category, count in category_count.items():
            file.write(f'{category}: {count}\n')