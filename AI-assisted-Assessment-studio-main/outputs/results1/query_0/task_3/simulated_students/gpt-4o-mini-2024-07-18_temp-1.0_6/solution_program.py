def analyze_game_results(input_file):
    results = {}
    with open(input_file, 'r') as file:
        for line in file:
            player_name, outcome = line.strip().split(',')
            if player_name not in results:
                results[player_name] = {'wins': 0, 'losses': 0}
            if outcome == 'win':
                results[player_name]['wins'] += 1
            elif outcome == 'lose':
                results[player_name]['losses'] += 1
    sorted_results = sorted(results.items())
    summary = []
    for player, counts in sorted_results:
        summary.append(f'{player}: {counts["wins"]}-{counts["losses"]}')
    return '\n'.join(summary)