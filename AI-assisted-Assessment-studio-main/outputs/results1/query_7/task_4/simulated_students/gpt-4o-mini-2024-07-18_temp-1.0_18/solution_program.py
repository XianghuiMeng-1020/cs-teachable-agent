def find_creatures_by_characteristic(filename, characteristic):
    creatures = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(':')
            if len(parts) > 1:
                name = parts[0].strip()
                characteristics = parts[1].strip().split(',')
                characteristics = [c.strip() for c in characteristics]
                if characteristic in characteristics:
                    creatures.append(name)
    return creatures