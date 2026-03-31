def find_creatures_by_characteristic(filename, characteristic):
    creature_names = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            name, characteristics = line.split(':')
            characteristics_list = characteristics.split(', ')
            if characteristic in characteristics_list:
                creature_names.append(name.strip())
    return creature_names