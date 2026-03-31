def find_creatures_by_attribute(file_path, attribute):
    creatures = []
    with open(file_path, 'r') as file:
        entries = file.read().strip().split('\n\n')
        for entry in entries:
            lines = entry.split('\n')
            if len(lines) >= 2:
                creature_name = lines[0].split(':')[0].strip()
                attributes_line = lines[1] if len(lines) > 1 else ''
                if 'Attributes:' in attributes_line:
                    attributes = attributes_line.split(':')[1].strip().split(', ')
                    if attribute in attributes:
                        creatures.append(creature_name)
    return creatures