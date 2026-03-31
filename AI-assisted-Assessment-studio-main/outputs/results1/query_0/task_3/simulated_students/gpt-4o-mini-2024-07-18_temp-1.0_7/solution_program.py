def analyze_game_results(input_file):
    results = {}

    with open(input_file, 'r') as file:
        for line in file:
            player, outcome = line.strip().split(',')
            if player not in results:
                results[player] = {'wins': 0, 'losses': 0}
            if outcome == 'win':
                results[player]['wins'] += 1
            elif outcome == 'lose':
                results[player]['losses'] += 1

    sorted_results = sorted(results.items())
    summary_lines = []
    for player, record in sorted_results:
        summary_lines.append(f'{player}: {record[