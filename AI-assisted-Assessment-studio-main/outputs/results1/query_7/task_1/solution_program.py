def find_creatures_by_attribute(file_path, attribute):
    with open(file_path, 'r') as file:
        content = file.read()
    sections = content.strip().split('\n\n')
    result = []
    for section in sections:
        lines = section.split('\n')
        if len(lines) != 2:
            continue
        name_line, attributes_line = lines
        name = name_line.split(':')[0].strip()
        attributes = attributes_line.split(':')[1].strip()
        attribute_list = [attr.strip() for attr in attributes.split(',')]
        if attribute in attribute_list:
            result.append(name)
    return result