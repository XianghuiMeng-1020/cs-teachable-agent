def find_creatures_by_attribute(file_path, attribute):
    creatures = []
    with open(file_path, 'r') as file:
        content = file.read().strip()
        entries = content.split('\n\n')
        for entry in entries:
            lines = entry.split('\n')
            if len(lines) >= 2:
                name_line = lines[0]
                attributes_line = lines[1]
                creature_name = name_line.split(':')[0].strip()
                attributes = attributes_line.split(':')[1].strip().split(', ')
                if attribute in attributes:
                    creatures.append(creature_name)
    return creatures