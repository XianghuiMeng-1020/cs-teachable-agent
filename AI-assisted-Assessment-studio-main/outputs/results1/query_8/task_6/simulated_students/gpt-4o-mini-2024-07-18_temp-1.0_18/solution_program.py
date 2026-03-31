def mythical_creature_classification(creatures):
    classification = {}
    for name, properties in creatures.items():
        danger_level = properties['danger_level']
        if danger_level < 3:
            classif = "Not Threatening"
        elif 3 <= danger_level <= 6:
            classif = "Moderately Threatening"
        else:
            classif = "Highly Threatening"

        if properties['favored_by'] == 'Zeus':
            classif += " - Zeus' favorite"

        classification[name] = classif

    return classification