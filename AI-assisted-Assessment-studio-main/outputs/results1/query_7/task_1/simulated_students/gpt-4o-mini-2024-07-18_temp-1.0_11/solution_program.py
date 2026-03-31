def find_creatures_by_attribute(file_path, attribute):
    creatures = []
    with open(file_path, 'r') as file:
        entries = file.read().strip().split('\n\n')
        for entry in entries:
            lines = entry.split('\n')
            if len(lines) >= 2:
                name = lines[0].split(':')[0].strip()
                attrs_line = lines[1]
                if attrs_line.startswith('Attributes:'):
                    attributes = attrs_line[len('Attributes:'):].strip().split(', ')
                    if attribute in attributes:
                        creatures.append(name)
    return creatures