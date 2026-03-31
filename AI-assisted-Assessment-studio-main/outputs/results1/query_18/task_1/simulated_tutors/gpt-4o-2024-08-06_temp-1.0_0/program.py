def calculate_total_energy():
    # Read integers from 'quantum_energy.txt'
    with open('quantum_energy.txt', 'r') as file:
        # Split the file contents into a list of strings, then convert to integers
        numbers = map(int, file.read().split())
        
    # Calculate the total energy level by summing the integers
    total_energy = sum(numbers)
    
    # Write the total sum to 'total_energy.txt'
    with open('total_energy.txt', 'w') as file:
        file.write(str(total_energy))