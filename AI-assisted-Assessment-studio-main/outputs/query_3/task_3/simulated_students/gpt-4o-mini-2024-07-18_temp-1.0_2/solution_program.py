def alien_population_change(data):
    current_populations = {}  
    for planet, changes in data.items():  
        current_population = 1.0  
        for change in changes:  
            change_value = int(change.split(':')[1]) / 1000  
            current_population += change_value  
        current_populations[planet] = round(current_population, 3)  
    return current_populations