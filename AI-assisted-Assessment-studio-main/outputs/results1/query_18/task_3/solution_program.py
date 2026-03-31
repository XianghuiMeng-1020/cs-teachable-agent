def calculate_fuel_for_mission(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        total_fuel = 0
        for line in lines:
            distance = int(line.strip())
            total_fuel += distance * 2
        with open('total_fuel.txt', 'w') as output_file:
            output_file.write(str(total_fuel) + '\n')