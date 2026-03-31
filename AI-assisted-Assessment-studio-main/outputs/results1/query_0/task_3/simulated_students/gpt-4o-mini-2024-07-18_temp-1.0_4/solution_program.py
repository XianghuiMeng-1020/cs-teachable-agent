def analyze_game_results(input_file):
    from collections import defaultdict
    
    results = defaultdict(lambda: {'wins': 0, 'losses': 0})
    
    with open(input_file, 'r') as file:
        for line in file:
            player_name, outcome = line.strip().split(',')
            if outcome == 'win':
                results[player_name]['wins'] += 1
            elif outcome == 'lose':
                results[player_name]['losses'] += 1
    
    sorted_results = sorted(results.items())
    summary_lines = []
    
    for player_name, outcome in sorted_results:
        wins = outcome['wins']
        losses = outcome['losses']
        summary_lines.append(f'{player_name}: {wins}-{losses}')
    
    return '\n'.join(summary_lines)