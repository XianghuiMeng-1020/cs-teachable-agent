def play_game_of_chance(board_positions, rolls):
    positions = {}
    for player, player_rolls in rolls.items():
        current_position = 0
        for roll in player_rolls:
            current_position = (current_position + roll) % board_positions
        positions[player] = current_position
    return positions