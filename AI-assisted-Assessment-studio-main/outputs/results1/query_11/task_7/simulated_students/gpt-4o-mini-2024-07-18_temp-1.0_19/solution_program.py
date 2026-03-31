def calculate_spices(dishes):
    spice_counts = {'Salad': 2, 'Soup': 3, 'Curry': 5, 'Grill': 7}
    total_spices = [0, 0, 0, 0]
    spice_map = {'Mild': 0, 'Medium': 1, 'Hot': 2, 'Extra Hot': 3}

    for dish in dishes:
        if dish in spice_counts:
            if dish == 'Salad':
                total_spices[spice_map['Mild']] += spice_counts[dish]
            elif dish == 'Soup':
                total_spices[spice_map['Medium']] += spice_counts[dish]
            elif dish == 'Curry':
                total_spices[spice_map['Hot']] += spice_counts[dish]
            elif dish == 'Grill':
                total_spices[spice_map['Extra Hot']] += spice_counts[dish]

    return total_spices