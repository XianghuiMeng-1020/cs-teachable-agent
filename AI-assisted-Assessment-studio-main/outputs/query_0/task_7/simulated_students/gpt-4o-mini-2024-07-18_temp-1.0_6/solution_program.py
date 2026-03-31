def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as winning_file:
            winning_numbers = winning_file.readline().strip().split(',')
            winning_numbers = set(winning_numbers)  # Use a set for faster lookups
    except FileNotFoundError:
        winning_numbers = set()

    results = []
    try:
        with open('players.txt', 'r') as players_file:
            for line in players_file:
                name, number = line.strip().split(',')
                match_count = 1 if number in winning_numbers else 0
                results.append(f'{name}: {match_count}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as results_file:
        results_file.write('\n'.join(results))