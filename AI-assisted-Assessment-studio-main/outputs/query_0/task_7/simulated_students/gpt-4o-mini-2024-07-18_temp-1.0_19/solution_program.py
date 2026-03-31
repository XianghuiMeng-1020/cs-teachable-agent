def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as win_file:
            winning_numbers = win_file.readline().strip().split(',')
            winning_numbers = set(map(str.strip, winning_numbers))
    except FileNotFoundError:
        winning_numbers = set()

    results = []
    try:
        with open('players.txt', 'r') as player_file:
            for line in player_file:
                name, number = line.strip().split(',')
                if number in winning_numbers:
                    count = 1
                else:
                    count = 0
                results.append(f'{name}: {count}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as result_file:
        result_file.write('\n'.join(results) + '\n')