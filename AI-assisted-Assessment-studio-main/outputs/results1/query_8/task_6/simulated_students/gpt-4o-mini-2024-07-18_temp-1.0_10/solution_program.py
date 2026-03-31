def mythical_creature_classification(creatures):
    classification = {}
    for creature, attributes in creatures.items():
        danger_level = attributes['danger_level']
        if danger_level < 3:
            classification[creature] = 'Not Threatening'
        elif 3 <= danger_level <= 6:
            classification[creature] = 'Moderately Threatening'
        else:
            classification[creature] = 'Highly Threatening'

        if attributes['favored_by'] == 'Zeus':
            classification[creature] += ' - Zeus'\' favorite'

    return classification