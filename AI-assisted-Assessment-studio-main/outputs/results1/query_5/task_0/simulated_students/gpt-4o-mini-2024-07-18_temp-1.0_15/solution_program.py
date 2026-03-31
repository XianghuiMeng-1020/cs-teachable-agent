def find_winner(filename):
    fastest_creature = None
    fastest_time = float('inf')
    with open(filename, 'r') as file:
        for line in file:
            name, time = line.strip().split(',')
            time = int(time)
            if time < fastest_time:
                fastest_time = time
                fastest_creature = name
    return fastest_creature