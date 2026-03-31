def calculate_spices(dishes):
    spice_requirements = {
        'Salad': 2,
        'Soup': 3,
        'Curry': 5,
        'Grill': 7
    }
    mild = 0
    medium = 0
    hot = 0
    extra_hot = 0
    for dish in dishes:
        if dish == 'Salad':
            mild += spice_requirements[dish]
        elif dish == 'Soup':
            medium += spice_requirements[dish]
        elif dish == 'Curry':
            hot += spice_requirements[dish]
        elif dish == 'Grill':
            extra_hot += spice_requirements[dish]
    return [mild, medium, hot, extra_hot]