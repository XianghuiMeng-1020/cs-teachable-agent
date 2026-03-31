def find_creatures_by_attribute(file_path, attribute):
    with open(file_path, 'r') as file:
        content = file.read()

    entries = content.strip().split('\n\n')
    matching_creatures = []

    for entry in entries:
        lines = entry.split('\n')
        creature_name = lines[0].split(':')[0].strip()
        attributes_line = lines[1].split(':')[1].strip() if len(lines) > 1 else ''
        attributes = [attr.strip() for attr in attributes_line.split(',')]  

        if attribute in attributes:
            matching_creatures.append(creature_name)

    return matching_creatures