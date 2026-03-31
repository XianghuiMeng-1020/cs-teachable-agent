def find_creatures_by_characteristic(filename, characteristic) -> list:
    creatures = []
    with open(filename, 'r') as file:
        for line in file:
            creature_info = line.strip().split(':')
            creature_name = creature_info[0].strip()
            characteristics = [char.strip() for char in creature_info[1].split(',')]
            if characteristic in characteristics:
                creatures.append(creature_name)
    return creatures
