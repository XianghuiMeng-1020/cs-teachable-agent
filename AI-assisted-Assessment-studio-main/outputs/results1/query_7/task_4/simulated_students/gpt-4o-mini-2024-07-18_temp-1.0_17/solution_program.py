def find_creatures_by_characteristic(filename, characteristic):
    creatures_with_characteristic = []
    with open(filename, 'r') as file:
        for line in file:
            creature, characteristics = line.split(':')
            characteristic_list = characteristics.strip().split(', ')
            if characteristic in characteristic_list:
                creatures_with_characteristic.append(creature.strip())
    return creatures_with_characteristic