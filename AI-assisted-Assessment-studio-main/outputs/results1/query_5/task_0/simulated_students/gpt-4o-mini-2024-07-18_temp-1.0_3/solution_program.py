def find_winner(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    fastest_time = float('inf')
    winner = None

    for line in lines:
        name, time = line.strip().split(',')
        time = int(time)
        if time < fastest_time:
            fastest_time = time
            winner = name

    return winner
