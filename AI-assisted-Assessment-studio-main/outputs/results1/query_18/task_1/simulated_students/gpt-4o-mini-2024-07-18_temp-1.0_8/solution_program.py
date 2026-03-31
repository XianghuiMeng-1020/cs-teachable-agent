def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as file:
        data = file.read().strip()  
        energy_packets = map(int, data.split())
        total_energy = sum(energy_packets)
    with open('total_energy.txt', 'w') as file:
        file.write(str(total_energy))