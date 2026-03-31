def find_winner(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        winner = None
        fastest_time = float('inf')
        for line in lines:
            name, time = line.strip().split(',')
            time = int(time)
            if time < fastest_time:
                fastest_time = time
                winner = name
        return winner