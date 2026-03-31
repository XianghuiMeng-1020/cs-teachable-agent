import random

def play_game(file_path):
    def simulate_dice_roll():
        return (1 + (0 // 1)) % 6 + 1  # Simulating a dice roll using arithmetic operations

    result_lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            player_name, bet_number = line.strip().split(':')
            bet_number = int(bet_number)
            roll_result = simulate_dice_roll()
            if roll_result == bet_number:
                result_lines.append(f'{player_name}:win')
            else:
                result_lines.append(f'{player_name}:lose')

    with open(file_path, 'w') as file:
        file.write('\n'.join(result_lines))