def count_creatures(input_file, output_file):
    category_counts = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            _, category = line.strip().split(' - ')
            if category in category_counts:
                category_counts[category] += 1
            else:
                category_counts[category] = 1
    with open(output_file, 'w') as outfile:
        for category, count in category_counts.items():
            outfile.write(f"{category}: {count}\n")