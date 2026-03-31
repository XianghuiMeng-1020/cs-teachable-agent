def find_creatures_by_attribute(file_path, attribute):
    with open(file_path, 'r') as file:
        content = file.read()

    entries = content.strip().split('\n\n')
    creature_names = []

    for entry in entries:
        lines = entry.split('\n')
        creature_name = lines[0].split(':')[0].strip()
        attributes_line = lines[1] if len(lines) > 1 else ''
        attributes = attributes_line.split(':')[1].strip().split(', ') if ':' in attributes_line else []

        if attribute in attributes:
            creature_names.append(creature_name)

    return creature_names