def mythical_creature_classification(creatures):
    classifications = {}
    for creature, attributes in creatures.items():
        danger_level = attributes['danger_level']
        classification = ''
        if danger_level < 3:
            classification = 'Not Threatening'
        elif 3 <= danger_level <= 6:
            classification = 'Moderately Threatening'
        else:
            classification = 'Highly Threatening'
        if attributes['favored_by'] == 'Zeus':
            classification += ' - Zeus' + "' favorite"
        classifications[creature] = classification
    return classifications