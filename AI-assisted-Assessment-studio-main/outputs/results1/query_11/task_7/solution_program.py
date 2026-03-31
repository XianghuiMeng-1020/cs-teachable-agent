def calculate_spices(dishes):
    mild, medium, hot, extra_hot = 0, 0, 0, 0
    for dish in dishes:
        if dish == 'Salad':
            mild += 2
        elif dish == 'Soup':
            medium += 3
        elif dish == 'Curry':
            hot += 5
        elif dish == 'Grill':
            extra_hot += 7
    return [mild, medium, hot, extra_hot]