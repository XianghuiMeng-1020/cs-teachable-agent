def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as win_file:
            winning_numbers = win_file.readline().strip().split(',')
    except FileNotFoundError:
        winning_numbers = []

    players_results = []

    try:
        with open('players.txt', 'r') as players_file:
            for line in players_file:
                name, number = line.strip().split(',')
                matches = winning_numbers.count(number)
                players_results.append(f"{name}: {matches}")
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as results_file:
        for result in players_results:
            results_file.write(result + '\n')