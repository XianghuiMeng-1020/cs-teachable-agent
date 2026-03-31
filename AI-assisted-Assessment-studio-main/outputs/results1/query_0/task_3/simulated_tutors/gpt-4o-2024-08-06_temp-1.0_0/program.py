def analyze_game_results(input_file):
    results = {}
    
    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if line:  # Check to ensure it's not an empty line
                player_name, outcome = line.split(',')
                
                if player_name not in results:
                    results[player_name] = {'win': 0, 'lose': 0}
                
                if outcome == 'win':
                    results[player_name]['win'] += 1
                elif outcome == 'lose':
                    results[player_name]['lose'] += 1

    # Prepare the output string
    output_lines = []
    for player in sorted(results):
        win_loss_record = f"{results[player]['win']}-{results[player]['lose']}"
        output_lines.append(f"{player}: {win_loss_record}")
        
    return '\n'.join(output_lines)

# Execute unit tests
test_analyze_game_results_1()
test_analyze_game_results_2()
test_analyze_game_results_3()
test_analyze_game_results_4()
test_analyze_game_results_empty()