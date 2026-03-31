def play_game_of_chance(board_positions, rolls):
    positions = {player: 0 for player in rolls.keys()}
    
    for player, roll_sequence in rolls.items():
        for roll in roll_sequence:
            positions[player] = (positions[player] + roll) % board_positions
    
    return positions