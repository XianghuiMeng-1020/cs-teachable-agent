def count_creatures(input_file, output_file):
    category_count = {}
    
    with open(input_file, 'r') as file:
        lines = file.readlines()
        
        for line in lines:
            # Split the line at the dash and strip any whitespace
            _, category = line.split('-')
            category = category.strip()
            
            # Count the occurrences of each category
            if category in category_count:
                category_count[category] += 1
            else:
                category_count[category] = 1
    
    with open(output_file, 'w') as file:
        for category, count in category_count.items():
            file.write(f'{category}: {count}\n')