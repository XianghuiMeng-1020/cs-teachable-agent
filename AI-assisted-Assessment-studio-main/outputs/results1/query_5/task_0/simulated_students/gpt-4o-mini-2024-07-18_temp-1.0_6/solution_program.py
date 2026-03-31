def find_winner(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    min_time = float('inf')
    winner = None

    for line in lines:
        name, time = line.strip().split(',')
        time = int(time)
        if time < min_time:
            min_time = time
            winner = name

    return winner