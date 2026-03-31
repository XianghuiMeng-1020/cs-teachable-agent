def calculate_spices(dishes):
    spice_count = [0, 0, 0, 0]
    spice_mapping = {
        'Salad': 2,   # Mild
        'Soup': 3,    # Medium
        'Curry': 5,   # Hot
        'Grill': 7     # Extra Hot
    }
    for dish in dishes:
        if dish in spice_mapping:
            spices_needed = spice_mapping[dish]
            if dish == 'Salad':
                spice_count[0] += spices_needed  # Mild
            elif dish == 'Soup':
                spice_count[1] += spices_needed  # Medium
            elif dish == 'Curry':
                spice_count[2] += spices_needed  # Hot
            elif dish == 'Grill':
                spice_count[3] += spices_needed  # Extra Hot
    return spice_count