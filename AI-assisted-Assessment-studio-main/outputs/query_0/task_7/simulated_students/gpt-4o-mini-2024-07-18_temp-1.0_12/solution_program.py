def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as w_file:
            winning_numbers = w_file.readline().strip().split(',')
    except FileNotFoundError:
        winning_numbers = []

    results = []

    try:
        with open('players.txt', 'r') as p_file:
            players = p_file.readlines()
    except FileNotFoundError:
        players = []

    for player in players:
        name, number = player.strip().split(',')
        match_count = winning_numbers.count(number)
        results.append(f'{name}: {match_count}')

    with open('results.txt', 'w') as r_file:
        for result in results:
            r_file.write(result + '\n')