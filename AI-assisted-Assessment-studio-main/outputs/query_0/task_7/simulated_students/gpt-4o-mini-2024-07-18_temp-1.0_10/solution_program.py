def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as win_file:
            winning_numbers = win_file.readline().strip().split(',')
            winning_numbers = [num.strip() for num in winning_numbers]
    except FileNotFoundError:
        winning_numbers = []

    results = []

    try:
        with open('players.txt', 'r') as players_file:
            players = players_file.readlines()
            for player in players:
                name, number = player.strip().split(',')
                number = number.strip()
                match_count = sum(1 for num in winning_numbers if num == number)
                results.append(f'{name}: {match_count}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as results_file:
        for result in results:
            results_file.write(result + '\n')