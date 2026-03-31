def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as infile:
        energy_packets = map(int, infile.read().split())
        total_energy = sum(energy_packets)
    with open('total_energy.txt', 'w') as outfile:
        outfile.write(str(total_energy))