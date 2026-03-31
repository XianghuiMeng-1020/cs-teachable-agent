def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as winning_file:
            winning_numbers = winning_file.readline().strip().split(',')
            winning_numbers = set(map(int, winning_numbers))
    except FileNotFoundError:
        winning_numbers = set()

    try:
        with open('players.txt', 'r') as players_file:
            players = players_file.readlines()
    except FileNotFoundError:
        players = []

    results = []
    for player in players:
        name, number = player.strip().split(',')
        chosen_number = int(number)
        matches = chosen_number in winning_numbers
        match_count = 1 if matches else 0
        results.append(f'{name}: {match_count}')

    with open('results.txt', 'w') as results_file:
        for result in results:
            results_file.write(result + '\n')