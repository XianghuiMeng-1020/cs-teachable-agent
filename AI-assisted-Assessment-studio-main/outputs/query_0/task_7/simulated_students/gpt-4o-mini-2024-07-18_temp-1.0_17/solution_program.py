def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as win_file:
            winning_numbers = win_file.readline().strip().split(',')
            winning_numbers = set(winning_numbers)  # Using a set for faster lookup
    except FileNotFoundError:
        winning_numbers = set()  # No winning numbers available

    results = []

    try:
        with open('players.txt', 'r') as players_file:
            for line in players_file:
                player_info = line.strip().split(',')
                if len(player_info) != 2:
                    continue  # Skip malformed lines
                player_name, player_number = player_info[0], player_info[1]
                if player_number in winning_numbers:
                    results.append(f'{player_name}: 1')
                else:
                    results.append(f'{player_name}: 0')
    except FileNotFoundError:
        pass  # No players available

    with open('results.txt', 'w') as results_file:
        for result in results:
            results_file.write(result + '\n')
