def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as infile:
        energy_data = infile.read().strip()
        energy_levels = map(int, energy_data.split())
        total_energy = sum(energy_levels)
    with open('total_energy.txt', 'w') as outfile:
        outfile.write(str(total_energy))