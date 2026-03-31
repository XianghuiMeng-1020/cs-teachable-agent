def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as winning_file:
            winning_numbers = winning_file.readline().strip().split(',')
            winning_numbers = set(map(int, winning_numbers))
    except FileNotFoundError:
        winning_numbers = set()

    results = []

    try:
        with open('players.txt', 'r') as players_file:
            for line in players_file:
                name, chosen_number = line.strip().split(',')
                chosen_number = int(chosen_number)
                matches = sum(1 for number in winning_numbers if number == chosen_number)
                results.append(f'{name}: {matches}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as results_file:
        results_file.write('\n'.join(results) + '\n')