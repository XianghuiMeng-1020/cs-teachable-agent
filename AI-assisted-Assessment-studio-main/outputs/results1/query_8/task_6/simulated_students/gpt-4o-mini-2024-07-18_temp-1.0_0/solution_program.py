def mythical_creature_classification(creatures):
    classification = {}
    for name, characteristics in creatures.items():
        danger_level = characteristics['danger_level']
        if danger_level < 3:
            classification[name] = 'Not Threatening'
        elif 3 <= danger_level <= 6:
            classification[name] = 'Moderately Threatening'
        else:
            classification[name] = 'Highly Threatening'

        if characteristics['favored_by'] == 'Zeus':
            classification[name] += ' - Zeus' + "'s favorite"

    return classification