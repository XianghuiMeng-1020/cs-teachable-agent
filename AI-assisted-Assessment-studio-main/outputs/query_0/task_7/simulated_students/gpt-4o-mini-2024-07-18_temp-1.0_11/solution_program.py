def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as win_file:
            winning_numbers = win_file.readline().strip().split(',')
            winning_numbers = set(winning_numbers)
    except FileNotFoundError:
        winning_numbers = set()

    results = []

    try:
        with open('players.txt', 'r') as players_file:
            lines = players_file.readlines()
            for line in lines:
                name, chosen_number = line.strip().split(',')
                matches = 1 if chosen_number in winning_numbers else 0
                results.append(f'{name}: {matches}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as results_file:
        for result in results:
            results_file.write(result + '\n')