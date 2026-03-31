def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as input_file:
        energy_packets = map(int, input_file.read().split())
        total_energy = sum(energy_packets)
    with open('total_energy.txt', 'w') as output_file:
        output_file.write(str(total_energy))