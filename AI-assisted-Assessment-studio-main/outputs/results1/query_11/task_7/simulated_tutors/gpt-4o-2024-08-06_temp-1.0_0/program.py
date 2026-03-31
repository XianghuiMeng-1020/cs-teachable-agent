def calculate_spices(dishes):
    # Initialize the spice amounts for each category
    mild = 0
    medium = 0
    hot = 0
    extra_hot = 0
    
    # Dictionary to map dishes to their spice requirements
    spice_requirements = {
        'Salad': 2,   # Mild spice
        'Soup': 3,    # Medium spice
        'Curry': 5,   # Hot spice
        'Grill': 7   # Extra Hot spice
    }

    # Iterate over each dish in the list
    for dish in dishes:
        if dish == 'Salad':
            mild += spice_requirements[dish]
        elif dish == 'Soup':
            medium += spice_requirements[dish]
        elif dish == 'Curry':
            hot += spice_requirements[dish]
        elif dish == 'Grill':
            extra_hot += spice_requirements[dish]
          
    # Return the total spice amounts in the specified order
    return [mild, medium, hot, extra_hot]