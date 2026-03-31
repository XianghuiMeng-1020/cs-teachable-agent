def find_creatures_by_attribute(file_path, attribute):
    creatures = []
    with open(file_path, 'r') as file:
        content = file.read().strip().split('\n\n')
        for entry in content:
            lines = entry.split('\n')
            if len(lines) < 2:
                continue
            name_line = lines[0]
            attributes_line = lines[1]
            creature_name = name_line.split(':')[0].strip()
            attributes = attributes_line.split(':')[1].strip().split(', ')
            if attribute in attributes:
                creatures.append(creature_name)
    return creatures