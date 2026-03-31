def find_creatures_by_attribute(file_path, attribute):
    with open(file_path, 'r') as file:
        content = file.read().strip()

    creatures = content.split('\n\n')
    result = []

    for creature in creatures:
        lines = creature.split('\n')
        if len(lines) < 2:
            continue
        name_line = lines[0]
        attributes_line = lines[1]

        creature_name = name_line.split(':')[0].strip()
        attributes = attributes_line.split(':')[1].strip().split(', ')

        if attribute in attributes:
            result.append(creature_name)

    return result