def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as wn_file:
            winning_numbers = wn_file.readline().strip().split(',')
    except FileNotFoundError:
        winning_numbers = []

    players_results = []

    try:
        with open('players.txt', 'r') as p_file:
            for line in p_file:
                name, chosen_number = line.strip().split(',')
                match_count = winning_numbers.count(chosen_number)
                players_results.append(f'{name}: {match_count}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as r_file:
        for result in players_results:
            r_file.write(result + '\n')