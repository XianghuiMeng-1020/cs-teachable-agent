def play_game_of_chance(board_positions, rolls):
    player_positions = {}
    for player, roll_list in rolls.items():
        position = 0
        for roll in roll_list:
            position += roll
            position %= board_positions  # Wrap around if exceeds board_positions
        player_positions[player] = position
    return player_positions