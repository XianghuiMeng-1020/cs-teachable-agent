def find_winner(filename):
    fastest_creature = None
    fastest_time = float('inf')
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            name = parts[0]
            time = int(parts[1])
            if time < fastest_time:
                fastest_time = time
                fastest_creature = name
    return fastest_creature