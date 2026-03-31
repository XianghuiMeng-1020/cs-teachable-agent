def play_game_of_chance(board_positions, rolls):
    final_positions = {}
    
    for player, player_rolls in rolls.items():
        position = 0  # start at position 0
        for roll in player_rolls:
            position += roll  # update position based on the roll
            if position >= board_positions:
                position = position % board_positions  # wrap around if needed
        final_positions[player] = position  # store player's final position
    
    return final_positions