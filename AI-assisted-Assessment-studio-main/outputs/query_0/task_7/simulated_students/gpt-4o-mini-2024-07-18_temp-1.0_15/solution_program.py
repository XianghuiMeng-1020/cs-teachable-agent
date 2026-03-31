def lucky_numbers():
    try:
        with open('winning_numbers.txt', 'r') as winning_file:
            winning_numbers = winning_file.readline().strip().split(',')
    except FileNotFoundError:
        winning_numbers = []

    player_results = []

    try:
        with open('players.txt', 'r') as players_file:
            players = players_file.readlines()
            for player in players:
                name, chosen_number = player.strip().split(',')
                chosen_number = chosen_number.strip()
                match_count = winning_numbers.count(chosen_number)
                player_results.append(f'{name}: {match_count}')
    except FileNotFoundError:
        pass

    with open('results.txt', 'w') as results_file:
        results_file.write('\n'.join(player_results) + '\n')