def calculate_total_energy():
    with open('quantum_energy.txt', 'r') as input_file:
        data = input_file.read()
        packets = map(int, data.split())
        total_energy = sum(packets)
    with open('total_energy.txt', 'w') as output_file:
        output_file.write(str(total_energy))