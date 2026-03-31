def analyze_game_results(input_file):
    with open(input_file, 'r') as file:
        lines = file.readlines()

    results = {}

    for line in lines:
        player, outcome = line.strip().split(',')
        if player not in results:
            results[player] = {'win': 0, 'lose': 0}
        results[player][outcome] += 1

    summary_lines = []

    for player in sorted(results.keys()):
        wins = results[player]['win']
        losses = results[player]['lose']
        summary_lines.append(f"{player}: {wins}-{losses}")

    return '\n'.join(summary_lines)