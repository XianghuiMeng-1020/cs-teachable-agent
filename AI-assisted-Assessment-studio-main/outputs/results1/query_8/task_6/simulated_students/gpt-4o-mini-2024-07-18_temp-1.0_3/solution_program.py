def mythical_creature_classification(creatures):
    classification = {}
    for creature, attributes in creatures.items():
        danger_level = attributes['danger_level']
        if danger_level < 3:
            class_name = 'Not Threatening'
        elif 3 <= danger_level <= 6:
            class_name = 'Moderately Threatening'
        else:
            class_name = 'Highly Threatening'
        if attributes['favored_by'] == 'Zeus':
            class_name += ' - Zeus'\u0027 favorite'
        classification[creature] = class_name
    return classification