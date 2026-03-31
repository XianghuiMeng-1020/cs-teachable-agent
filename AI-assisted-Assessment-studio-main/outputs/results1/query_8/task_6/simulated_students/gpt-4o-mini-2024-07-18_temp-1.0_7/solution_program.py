def mythical_creature_classification(creatures):
    classification = {}
    for creature, attributes in creatures.items():
        danger_level = attributes['danger_level']
        classification_string = ""
        if danger_level < 3:
            classification_string = "Not Threatening"
        elif 3 <= danger_level <= 6:
            classification_string = "Moderately Threatening"
        else:
            classification_string = "Highly Threatening"
        if attributes['favored_by'] == 'Zeus':
            classification_string += " - Zeus' favorite"
        classification[creature] = classification_string
    return classification