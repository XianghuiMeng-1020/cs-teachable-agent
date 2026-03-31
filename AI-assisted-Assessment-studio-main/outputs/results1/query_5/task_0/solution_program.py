def find_winner(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    winners_time = float('inf')
    winner_name = ''
    for line in lines:
        name, time_str = line.strip().split(',')
        time = int(time_str)
        if time < winners_time:
            winners_time = time
            winner_name = name
    return winner_name
