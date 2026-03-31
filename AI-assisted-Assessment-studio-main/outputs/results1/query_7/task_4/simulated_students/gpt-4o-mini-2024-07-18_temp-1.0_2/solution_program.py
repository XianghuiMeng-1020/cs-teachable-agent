def find_creatures_by_characteristic(filename, characteristic):
    unique_creatures = []
    with open(filename, 'r') as file:
        for line in file:
            creature_info = line.strip().split(':')
            creature_name = creature_info[0]
            characteristics = creature_info[1].split(', ')
            if characteristic in characteristics:
                unique_creatures.append(creature_name)
    return unique_creatures