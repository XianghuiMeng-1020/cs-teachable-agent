def find_creatures_by_attribute(file_path, attribute):
    with open(file_path, 'r') as file:
        content = file.read().strip().split('\n\n')

    matching_creatures = []

    for entry in content:
        if attribute in entry:
            lines = entry.split('\n')
            creature_name = lines[0].split(':')[0].strip()
            attributes_line = lines[1]
            attributes = attributes_line.split(':')[1].strip().split(', ')
            if attribute in [a.strip() for a in attributes]:
                matching_creatures.append(creature_name)

    return matching_creatures