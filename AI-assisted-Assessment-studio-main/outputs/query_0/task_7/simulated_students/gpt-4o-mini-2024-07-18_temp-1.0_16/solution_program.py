def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as win_file:
            winning_numbers = win_file.readline().strip().split(',')
    except FileNotFoundError:
        winning_numbers = []

    results = []
    try:
        with open('players.txt', 'r') as players_file:
            for line in players_file:
                player_name, player_number = line.strip().split(',')
                if player_number in winning_numbers:
                    results.append(f'{player_name}: 1')
                else:
                    results.append(f'{player_name}: 0')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as results_file:
        for result in results:
            results_file.write(result + '\n')