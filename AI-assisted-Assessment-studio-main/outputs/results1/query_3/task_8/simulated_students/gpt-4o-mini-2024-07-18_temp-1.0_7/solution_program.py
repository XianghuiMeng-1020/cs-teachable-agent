def play_game_of_chance(board_positions, rolls):
    final_positions = {}
    
    for player, player_rolls in rolls.items():
        position = 0
        for roll in player_rolls:
            position += roll
            position %= board_positions  # Loop back if position exceeds board
        final_positions[player] = position
    
    return final_positions