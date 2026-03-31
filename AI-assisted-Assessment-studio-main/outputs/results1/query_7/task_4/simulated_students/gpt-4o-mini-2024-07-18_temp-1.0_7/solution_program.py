def find_creatures_by_characteristic(filename, characteristic):
    creatures = []
    with open(filename, 'r') as file:
        for line in file:
            name, traits = line.strip().split(': ')
            if characteristic in traits.split(', '):
                creatures.append(name)
    return creatures