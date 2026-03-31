def calculate_spices(dishes):
    spice_requirements = {
        'Salad': 2,  
        'Soup': 3,  
        'Curry': 5,  
        'Grill': 7
    }
    total_spices = [0, 0, 0, 0]  # Mild, Medium, Hot, Extra Hot

    for dish in dishes:
        if dish == 'Salad':
            total_spices[0] += spice_requirements[dish]
        elif dish == 'Soup':
            total_spices[1] += spice_requirements[dish]
        elif dish == 'Curry':
            total_spices[2] += spice_requirements[dish]
        elif dish == 'Grill':
            total_spices[3] += spice_requirements[dish]

    return total_spices