def find_creatures_by_attribute(file_path, attribute):
    creatures_with_attribute = []
    with open(file_path, 'r') as file:
        entries = file.read().strip().split('\n\n')
        for entry in entries:
            lines = entry.split('\n')
            creature_name = lines[0].split(':')[0].strip()
            attributes_line = lines[1].split(':')[1].strip() if len(lines) > 1 else ''
            attributes = [attr.strip() for attr in attributes_line.split(',')] 
            if attribute in attributes:
                creatures_with_attribute.append(creature_name)
    return creatures_with_attribute