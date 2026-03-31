def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as file:
        energy_packets = file.read().strip().split()
        total_energy = sum(int(packet) for packet in energy_packets)
    with open('total_energy.txt', 'w') as output_file:
        output_file.write(str(total_energy))