def find_winner(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    fastest_creature = None
    fastest_time = float('inf')
    for line in lines:
        name, time = line.strip().split(',')
        time = int(time)
        if time < fastest_time:
            fastest_time = time
            fastest_creature = name
    return fastest_creature
