def find_creatures_by_characteristic(filename, characteristic) -> list:
    with open(filename, 'r') as file:
        lines = file.readlines()

    creatures = []
    for line in lines:
        creature, characteristics = line.split(':')
        characteristics_list = [c.strip() for c in characteristics.split(',')]
        if characteristic in characteristics_list:
            creatures.append(creature.strip())

    return creatures