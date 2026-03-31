def find_creatures_by_characteristic(filename, characteristic):
    creatures = []
    with open(filename, 'r') as file:
        for line in file:
            creature, characteristics = line.split(':')
            if characteristic in characteristics.split(', '):
                creatures.append(creature)
    return creatures