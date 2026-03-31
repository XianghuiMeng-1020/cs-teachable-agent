def find_creatures_by_attribute(file_path, attribute):
    creatures = []
    with open(file_path, 'r') as file:
        content = file.read().strip().split('\n\n')
        for entry in content:
            lines = entry.split('\n')
            if len(lines) < 2:
                continue
            creature_name = lines[0].split(': ')[0]
            attributes_line = lines[1]
            if 'Attributes:' in attributes_line:
                attributes = attributes_line.split(': ')[1].strip().split(', ')
                if attribute in attributes:
                    creatures.append(creature_name)
    return creatures