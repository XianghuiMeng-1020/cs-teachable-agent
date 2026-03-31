def find_creatures_by_characteristic(filename, characteristic):
    creatures_with_characteristic = []
    with open(filename, 'r') as file:
        for line in file:
            creature_info = line.strip().split(': ')
            creature_name = creature_info[0]
            characteristics = creature_info[1].split(', ')
            if characteristic in characteristics:
                creatures_with_characteristic.append(creature_name)
    return creatures_with_characteristic