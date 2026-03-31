def find_creatures_by_characteristic(filename, characteristic):
    creatures = []
    with open(filename, 'r') as file:
        for line in file:
            name, characteristics = line.split(':')
            if characteristic in characteristics:
                creatures.append(name.strip())
    return creatures