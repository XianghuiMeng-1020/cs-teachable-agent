def calculate_spices(dishes):
    spice_requirements = {
        'Salad': (2, 0, 0, 0),
        'Soup': (0, 3, 0, 0),
        'Curry': (0, 0, 5, 0),
        'Grill': (0, 0, 0, 7)
    }
    total_spices = [0, 0, 0, 0]

    for dish in dishes:
        if dish in spice_requirements:
            requirements = spice_requirements[dish]
            total_spices[0] += requirements[0]
            total_spices[1] += requirements[1]
            total_spices[2] += requirements[2]
            total_spices[3] += requirements[3]

    return total_spices