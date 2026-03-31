def mythical_creature_classification(creatures):
    result = {}
    for name, attributes in creatures.items():
        danger = attributes['danger_level']
        favored = attributes['favored_by']
        if danger < 3:
            classification = "Not Threatening"
        elif 3 <= danger <= 6:
            classification = "Moderately Threatening"
        else:
            classification = "Highly Threatening"
        if favored == "Zeus":
            classification += " - Zeus' favorite"
        result[name] = classification
    return result
