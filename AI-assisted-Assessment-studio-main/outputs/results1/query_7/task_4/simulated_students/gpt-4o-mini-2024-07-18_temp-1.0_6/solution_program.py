def find_creatures_by_characteristic(filename, characteristic):
    unique_creatures = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            creature_name, characteristics = line.split(':')
            characteristics_list = [c.strip() for c in characteristics.split(',')]
            if characteristic in characteristics_list:
                unique_creatures.append(creature_name)
    return unique_creatures