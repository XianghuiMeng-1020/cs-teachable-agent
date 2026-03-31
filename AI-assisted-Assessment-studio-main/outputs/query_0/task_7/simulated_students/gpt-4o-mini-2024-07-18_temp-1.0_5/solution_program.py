def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as wn_file:
            winning_numbers = wn_file.read().strip().split(',')
    except FileNotFoundError:
        winning_numbers = []

    players_results = []
    try:
        with open('players.txt', 'r') as players_file:
            for line in players_file:
                if line.strip():
                    name, number = line.strip().split(',')
                    matched_count = 1 if number in winning_numbers else 0
                    players_results.append(f'{name}: {matched_count}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as results_file:
        for result in players_results:
            results_file.write(result + '\n')
