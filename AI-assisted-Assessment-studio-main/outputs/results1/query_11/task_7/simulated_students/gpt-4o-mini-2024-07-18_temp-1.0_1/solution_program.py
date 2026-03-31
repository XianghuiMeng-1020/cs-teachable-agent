def calculate_spices(dishes):
    spices = {'Salad': 2, 'Soup': 3, 'Curry': 5, 'Grill': 7}
    total_spices = [0, 0, 0, 0]
    spice_order = ['Mild', 'Medium', 'Hot', 'Extra Hot']

    for dish in dishes:
        if dish in spices:
            index = spice_order.index(spice_order[list(spices.keys()).index(dish)])
            total_spices[index] += spices[dish]

    return total_spices