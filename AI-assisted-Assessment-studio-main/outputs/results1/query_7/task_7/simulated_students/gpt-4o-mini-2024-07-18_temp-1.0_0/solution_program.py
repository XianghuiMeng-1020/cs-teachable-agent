def count_creatures(input_file, output_file):
    category_count = {}
    
    with open(input_file, 'r') as file:
        for line in file:
            # Split the line on the dash to separate the name and category
            name, category = line.strip().split(' - ')
            
            # Increment the count for the category
            if category in category_count:
                category_count[category] += 1
            else:
                category_count[category] = 1
    
    with open(output_file, 'w') as file:
        for category, count in category_count.items():
            file.write(f'{category}: {count}\n')