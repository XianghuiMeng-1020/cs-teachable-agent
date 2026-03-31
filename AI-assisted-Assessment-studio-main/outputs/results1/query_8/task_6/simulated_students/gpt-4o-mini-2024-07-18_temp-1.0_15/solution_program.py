def mythical_creature_classification(creatures):
    classification = {} 
    for creature, attributes in creatures.items():
        danger_level = attributes['danger_level']
        result = ''
        if danger_level < 3:
            result = 'Not Threatening'
        elif 3 <= danger_level <= 6:
            result = 'Moderately Threatening'
        else:
            result = 'Highly Threatening'
        if attributes['favored_by'] == 'Zeus':
            result += ' - Zeus' favorite'
        classification[creature] = result
    return classification