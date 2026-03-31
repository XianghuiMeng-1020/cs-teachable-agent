def alien_population_change(data):
    # Initial population in millions
    initial_population = 1.0
    result = {}
    
    # Iterate over each planet and its changes
    for planet, changes in data.items():
        current_population = initial_population
        
        # Process each year's change
        for entry in changes:
            year, change = entry.split(':')
            change = int(change) / 1000  # Convert to millions
            
            # Update current population
            current_population += change
        
        # Store the result for the current planet
        result[planet] = current_population
    
    return result

# Example usage: The function can be tested and debugged with appropriate data as hinted by the test cases