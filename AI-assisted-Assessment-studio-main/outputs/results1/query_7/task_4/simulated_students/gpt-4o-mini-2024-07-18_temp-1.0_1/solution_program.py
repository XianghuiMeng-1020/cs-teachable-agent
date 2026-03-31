def find_creatures_by_characteristic(filename, characteristic):
    creatures = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) == 2:
                creature_name = parts[0] 
                characteristics = parts[1].split(',')
                characteristics = [char.strip() for char in characteristics]  
                if characteristic in characteristics:
                    creatures.append(creature_name)
    return creatures