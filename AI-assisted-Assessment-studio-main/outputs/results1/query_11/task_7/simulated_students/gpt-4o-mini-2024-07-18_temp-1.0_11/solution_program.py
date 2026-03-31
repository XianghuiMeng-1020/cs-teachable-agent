def calculate_spices(dishes):
    spice_requirements = {
        'Salad': 2,
        'Soup': 3,
        'Curry': 5,
        'Grill': 7
    }
    total_mild = 0
    total_medium = 0
    total_hot = 0
    total_extra_hot = 0

    for dish in dishes:
        if dish == 'Salad':
            total_mild += spice_requirements[dish]
        elif dish == 'Soup':
            total_medium += spice_requirements[dish]
        elif dish == 'Curry':
            total_hot += spice_requirements[dish]
        elif dish == 'Grill':
            total_extra_hot += spice_requirements[dish]

    return [total_mild, total_medium, total_hot, total_extra_hot]