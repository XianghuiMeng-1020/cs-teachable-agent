def find_creatures_by_characteristic(filename, characteristic):
    creatures = []
    with open(filename, 'r') as file:
        for line in file:
            creature_info = line.strip().split(': ')
            if len(creature_info) > 1:
                creature_name = creature_info[0]
                characteristics = creature_info[1].split(', ')
                if characteristic in characteristics:
                    creatures.append(creature_name)
    return creatures