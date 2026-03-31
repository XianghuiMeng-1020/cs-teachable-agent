def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as infile:
        data = infile.read().strip()
        energy_packets = map(int, data.split())
        total_energy = sum(energy_packets)
    with open('total_energy.txt', 'w') as outfile:
        outfile.write(str(total_energy))