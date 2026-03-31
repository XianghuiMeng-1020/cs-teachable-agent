def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as winning_file:
            winning_numbers = winning_file.readline().strip().split(',')
    except (FileNotFoundError, IndexError):
        winning_numbers = []

    try:
        with open('players.txt', 'r') as players_file:
            players = players_file.readlines()
    except FileNotFoundError:
        players = []

    results = []
    for player in players:
        name, chosen_number = player.strip().split(',')
        matches = 0
        if chosen_number in winning_numbers:
            matches = 1
        results.append(f'{name}: {matches}')

    with open('results.txt', 'w') as results_file:
        results_file.write('\n'.join(results))