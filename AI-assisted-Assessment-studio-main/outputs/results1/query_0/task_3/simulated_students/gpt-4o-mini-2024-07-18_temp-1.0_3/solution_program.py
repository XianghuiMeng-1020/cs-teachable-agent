def analyze_game_results(input_file):
    results = {}
    with open(input_file, 'r') as file:
        for line in file:
            player, outcome = line.strip().split(',')
            if player not in results:
                results[player] = {'wins': 0, 'losses': 0}
            if outcome == 'win':
                results[player]['wins'] += 1
            else:
                results[player]['losses'] += 1

    output = []
    for player in sorted(results.keys()):
        wins = results[player]['wins']
        losses = results[player]['losses']
        output.append(f'{player}: {wins}-{losses}')

    return '\n'.join(output)