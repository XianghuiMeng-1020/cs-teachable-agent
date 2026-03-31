def mythical_creature_classification(creatures):
    classification = {}
    for creature, attributes in creatures.items():
        danger_level = attributes['danger_level']
        classification_str = ''

        if danger_level < 3:
            classification_str = 'Not Threatening'
        elif 3 <= danger_level <= 6:
            classification_str = 'Moderately Threatening'
        else:
            classification_str = 'Highly Threatening'

        if attributes['favored_by'] == 'Zeus':
            classification_str += ' - Zeus' + "'" + ' favorite'

        classification[creature] = classification_str
    return classification