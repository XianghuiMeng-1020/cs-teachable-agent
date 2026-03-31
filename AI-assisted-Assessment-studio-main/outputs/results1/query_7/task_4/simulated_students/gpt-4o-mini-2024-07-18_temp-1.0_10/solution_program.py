def find_creatures_by_characteristic(filename, characteristic):
    with open(filename, 'r') as file:
        lines = file.readlines()

    creatures = []
    for line in lines:
        creature, characteristics = line.split(':')
        characteristic_list = characteristics.strip().split(', ')
        if characteristic in characteristic_list:
            creatures.append(creature.strip())

    return creatures