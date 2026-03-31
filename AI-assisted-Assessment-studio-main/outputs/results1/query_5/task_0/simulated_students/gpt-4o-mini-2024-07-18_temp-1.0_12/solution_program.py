def find_winner(filename):
    fastest_time = float('inf')
    winner = None
    with open(filename, 'r') as file:
        for line in file:
            creature, time = line.strip().split(',')
            time = int(time)
            if time < fastest_time:
                fastest_time = time
                winner = creature
    return winner