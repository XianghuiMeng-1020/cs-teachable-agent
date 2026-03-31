def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as win_file:
            winning_numbers = win_file.readline().strip().split(',')
            winning_numbers = set(winning_numbers)  # Convert to set for faster lookup
    except FileNotFoundError:
        winning_numbers = set()  # Handle case when the file doesn't exist

    results = []
    try:
        with open('players.txt', 'r') as player_file:
            for line in player_file:
                name, number = line.strip().split(',')
                if number in winning_numbers:
                    results.append(f'{name}: 1')
                else:
                    results.append(f'{name}: 0')
    except FileNotFoundError:
        pass  # Handle case when the players file doesn't exist

    with open('results.txt', 'w') as result_file:
        result_file.write('\n'.join(results))