def lucky_numbers():
    try:
        with open('players.txt', 'r') as players_file:
            players = players_file.readlines()
    except FileNotFoundError:
        players = []

    try:
        with open('winning_numbers.txt', 'r') as winning_file:
            winning_numbers = winning_file.readline().strip().split(',')
            winning_numbers = set(winning_numbers)
    except FileNotFoundError:
        winning_numbers = set()

    results = []
    for player in players:
        name, number = player.strip().split(',')
        if number in winning_numbers:
            results.append(f'{name}: 1')
        else:
            results.append(f'{name}: 0')

    with open('results.txt', 'w') as results_file:
        for result in results:
            results_file.write(result + '\n')
