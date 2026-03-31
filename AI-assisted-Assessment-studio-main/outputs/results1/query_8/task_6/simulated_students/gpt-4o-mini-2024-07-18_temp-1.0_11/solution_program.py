def mythical_creature_classification(creatures):
    classifications = {}
    for creature, characteristics in creatures.items():
        danger_level = characteristics['danger_level']
        classification = ''
        if danger_level < 3:
            classification = 'Not Threatening'
        elif 3 <= danger_level <= 6:
            classification = 'Moderately Threatening'
        else:
            classification = 'Highly Threatening'

        if characteristics['favored_by'] == 'Zeus':
            classification += ' - Zeus' + "' favorite"

        classifications[creature] = classification
    return classifications