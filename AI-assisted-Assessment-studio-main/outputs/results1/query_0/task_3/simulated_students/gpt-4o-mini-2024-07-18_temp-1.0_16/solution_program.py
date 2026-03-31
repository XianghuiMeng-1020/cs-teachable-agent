def analyze_game_results(input_file):
    from collections import defaultdict
    
    results = defaultdict(lambda: {'wins': 0, 'losses': 0})
    
    with open(input_file, 'r') as file:
        for line in file:
            player, outcome = line.strip().split(',')
            if outcome == 'win':
                results[player]['wins'] += 1
            elif outcome == 'lose':
                results[player]['losses'] += 1
    
    summary = []
    for player in sorted(results.keys()):
        wins = results[player]['wins']
        losses = results[player]['losses']
        summary.append(f"{player}: {wins}-{losses}")
    
    return '\n'.join(summary)