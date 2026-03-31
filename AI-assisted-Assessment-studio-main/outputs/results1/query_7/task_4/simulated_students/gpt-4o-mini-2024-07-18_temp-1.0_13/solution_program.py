def find_creatures_by_characteristic(filename, characteristic):
    creatures_with_characteristic = []
    with open(filename, 'r') as file:
        for line in file:
            creature_data = line.strip().split(': ')
            if len(creature_data) == 2:
                creature_name = creature_data[0]
                characteristics = creature_data[1].split(', ')
                if characteristic in characteristics:
                    creatures_with_characteristic.append(creature_name)
    return creatures_with_characteristic