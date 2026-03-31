def count_creatures(input_file, output_file):
    category_count = {}
    
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if '-' in line:
                creature, category = line.split(' - ')
                category = category.strip()
                if category in category_count:
                    category_count[category] += 1
                else:
                    category_count[category] = 1
    
    with open(output_file, 'w') as out_file:
        for category, count in category_count.items():
            out_file.write(f'{category}: {count}\n')