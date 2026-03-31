def play_game_of_chance(board_positions, rolls):
    positions = {player: 0 for player in rolls}
    
    for player, roll_list in rolls.items():
        for roll in roll_list:
            positions[player] = (positions[player] + roll) % board_positions
    
    return positions