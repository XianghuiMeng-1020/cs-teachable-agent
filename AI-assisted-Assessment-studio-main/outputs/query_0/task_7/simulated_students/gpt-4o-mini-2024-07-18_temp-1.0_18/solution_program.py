def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as wn_file:
            winning_numbers = wn_file.readline().strip().split(',')
    except FileNotFoundError:
        winning_numbers = []

    results = []

    try:
        with open('players.txt', 'r') as players_file:
            for line in players_file:
                name, chosen_number = line.strip().split(',')
                matches = winning_numbers.count(chosen_number)
                results.append(f'{name}: {matches}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as results_file:
        for result in results:
            results_file.write(result + '\n')