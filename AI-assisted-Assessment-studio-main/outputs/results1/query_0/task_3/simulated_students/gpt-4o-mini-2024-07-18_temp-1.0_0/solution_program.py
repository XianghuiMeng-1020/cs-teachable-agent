def analyze_game_results(input_file):
    from collections import defaultdict
    
    game_results = defaultdict(lambda: {'wins': 0, 'losses': 0})
    
    with open(input_file, 'r') as file:
        for line in file:
            player, outcome = line.strip().split(',')
            if outcome == 'win':
                game_results[player]['wins'] += 1
            elif outcome == 'lose':
                game_results[player]['losses'] += 1

    result_lines = []
    for player in sorted(game_results.keys()):
        wins = game_results[player]['wins']
        losses = game_results[player]['losses']
        result_lines.append(f"{player}: {wins}-{losses}")
    
    return '\n'.join(result_lines)