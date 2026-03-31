def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as win_file:
            winning_numbers = win_file.read().strip().split(',')
    except FileNotFoundError:
        winning_numbers = []

    results = []
    try:
        with open('players.txt', 'r') as player_file:
            for line in player_file:
                name, number = line.strip().split(',')
                matches = winning_numbers.count(number)
                results.append(f'{name}: {matches}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as result_file:
        for result in results:
            result_file.write(result + '\n')