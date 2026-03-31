def mythical_creature_classification(creatures):
    classification = {}
    for creature, traits in creatures.items():
        danger_level = traits['danger_level']
        if danger_level < 3:
            class_type = "Not Threatening"
        elif 3 <= danger_level <= 6:
            class_type = "Moderately Threatening"
        else:
            class_type = "Highly Threatening"

        if traits['favored_by'] == 'Zeus':
            class_type += " - Zeus' favorite"

        classification[creature] = class_type
    return classification