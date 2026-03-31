def lucky_numbers():
    with open('players.txt', 'r') as players_file:
        players_lines = players_file.readlines()
        
    with open('winning_numbers.txt', 'r') as winning_file:
        winning_numbers = [int(n) for n in winning_file.readline().strip().split(',')]
        
    results = []
    for line in players_lines:
        name, number_str = line.strip().split(',')
        player_number = int(number_str)
        matches = sum(1 for num in winning_numbers if num == player_number)
        results.append(f"{name}: {matches}\n")
        
    with open('results.txt', 'w') as results_file:
        results_file.writelines(results)