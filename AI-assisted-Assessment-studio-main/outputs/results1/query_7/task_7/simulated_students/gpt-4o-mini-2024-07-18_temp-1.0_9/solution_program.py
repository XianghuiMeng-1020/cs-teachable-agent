def count_creatures(input_file, output_file):
    creature_count = {}
    with open(input_file, 'r') as infile:
        for line in infile:
            line = line.strip()
            if ' - ' in line:
                _, category = line.split(' - ', 1)
                category = category.strip()
                if category in creature_count:
                    creature_count[category] += 1
                else:
                    creature_count[category] = 1
    with open(output_file, 'w') as outfile:
        for category, count in creature_count.items():
            outfile.write(f'{category}: {count}\n')