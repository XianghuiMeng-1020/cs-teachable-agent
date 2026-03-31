import random

def play_game(file_path):
    with open(file_path, 'r') as file:
        game_data = file.readlines()
    results = []
    
    for line in game_data:
        player_name, bet_number = line.strip().split(':')
        bet_number = int(bet_number)
        # Simulate dice roll
        roll = (random.randint(1, 6))
        # Check win or lose
        if roll == bet_number:
            results.append(f'{player_name}:win')
        else:
            results.append(f'{player_name}:lose')
    
    with open(file_path, 'w') as file:
        for result in results:
            file.write(result + '\n')