def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as win_file:
            winning_numbers = win_file.readline().strip().split(',')
    except FileNotFoundError:
        winning_numbers = []

    results = []

    try:
        with open('players.txt', 'r') as player_file:
            players = player_file.readlines()
            
            for player in players:
                name, number = player.strip().split(',')
                matches = 1 if number in winning_numbers else 0
                results.append(f'{name}: {matches}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as result_file:
        for result in results:
            result_file.write(result + '\n')