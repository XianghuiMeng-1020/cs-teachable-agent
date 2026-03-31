def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as file:
        energy_packets = map(int, file.read().split())
        total_energy = sum(energy_packets)
    with open('total_energy.txt', 'w') as file:
        file.write(str(total_energy))
