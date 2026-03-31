def mythical_creature_classification(creatures):
    classification = {}
    for name, attributes in creatures.items():
        danger_level = attributes['danger_level']
        if danger_level < 3:
            classification[name] = "Not Threatening"
        elif 3 <= danger_level <= 6:
            classification[name] = "Moderately Threatening"
        else:
            classification[name] = "Highly Threatening"

        if attributes['favored_by'] == 'Zeus':
            classification[name] += " - Zeus' favorite"

    return classification