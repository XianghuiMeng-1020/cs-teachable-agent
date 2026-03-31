def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as file:
        data = file.read().strip()
    energy_values = map(int, data.split())
    total_energy = sum(energy_values)
    with open('total_energy.txt', 'w') as file:
        file.write(str(total_energy))