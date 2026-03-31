def count_creatures(input_file, output_file):
    counts = {}
    with open(input_file, 'r') as file:
        for line in file:
            creature_info = line.strip().split(' - ')
            if len(creature_info) == 2:
                category = creature_info[1]
                if category in counts:
                    counts[category] += 1
                else:
                    counts[category] = 1
    with open(output_file, 'w') as file:
        for category, count in counts.items():
            file.write(f"{category}: {count}\n")