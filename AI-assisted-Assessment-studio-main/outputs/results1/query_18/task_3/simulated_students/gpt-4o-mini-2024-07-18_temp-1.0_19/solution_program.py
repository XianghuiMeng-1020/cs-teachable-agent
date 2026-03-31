def calculate_fuel_for_mission(filename):
    total_fuel = 0
    with open(filename, 'r') as file:
        for line in file:
            distance = int(line.strip())
            total_fuel += distance * 2
    with open('total_fuel.txt', 'w') as f:
        f.write(str(total_fuel))