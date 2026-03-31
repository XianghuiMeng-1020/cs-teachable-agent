def mythical_creature_classification(creatures):
    classification = {}
    for creature, attributes in creatures.items():
        danger_level = attributes['danger_level']
        if danger_level < 3:
            classif = "Not Threatening"
        elif 3 <= danger_level <= 6:
            classif = "Moderately Threatening"
        else:
            classif = "Highly Threatening"
        if attributes['favored_by'] == 'Zeus':
            classif += " - Zeus' favorite"
        classification[creature] = classif
    return classification