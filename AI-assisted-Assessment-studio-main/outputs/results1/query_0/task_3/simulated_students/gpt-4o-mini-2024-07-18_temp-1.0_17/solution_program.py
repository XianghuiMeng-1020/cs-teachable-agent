def analyze_game_results(input_file):
    game_results = {}

    with open(input_file, 'r') as file:
        for line in file:
            player, outcome = line.strip().split(',')
            if player not in game_results:
                game_results[player] = {'wins': 0, 'losses': 0}
            if outcome == 'win':
                game_results[player]['wins'] += 1
            elif outcome == 'lose':
                game_results[player]['losses'] += 1

    results = []
    for player in sorted(game_results.keys()):
        wins = game_results[player]['wins']
        losses = game_results[player]['losses']
        results.append(f"{player}: {wins}-{losses}")

    return '\n'.join(results)