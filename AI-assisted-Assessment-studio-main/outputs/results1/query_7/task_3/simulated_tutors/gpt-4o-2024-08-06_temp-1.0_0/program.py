def filter_mythical_creatures(input_filename, output_filename, status):
    with open(input_filename, 'r') as infile:
        lines = infile.readlines()
        
    filtered_creatures = []
    for line in lines:
        creature_data = line.strip().split(':')
        if len(creature_data) == 2:
            creature_name, legendary_status = creature_data
            if legendary_status.strip() == status:
                filtered_creatures.append(creature_name)
    
    with open(output_filename, 'w') as outfile:
        for creature in filtered_creatures:
            outfile.write(creature + '\n')