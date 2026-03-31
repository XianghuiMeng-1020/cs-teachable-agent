def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as infile:
        energy_packets = infile.read().strip().split()  
        total_energy = sum(int(packet) for packet in energy_packets)
    with open('total_energy.txt', 'w') as outfile:
        outfile.write(str(total_energy))