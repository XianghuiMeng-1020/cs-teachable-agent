def play_game_of_chance(board_positions, rolls):
    positions = {player: 0 for player in rolls.keys()}
    for player, roll_list in rolls.items():
        for roll in roll_list:
            positions[player] += roll
            if positions[player] >= board_positions:
                positions[player] = positions[player] % board_positions
    return positions