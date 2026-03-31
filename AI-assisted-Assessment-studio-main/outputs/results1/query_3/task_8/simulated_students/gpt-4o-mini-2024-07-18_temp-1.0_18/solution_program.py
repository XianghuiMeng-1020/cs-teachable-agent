def play_game_of_chance(board_positions, rolls):
    positions = {player: 0 for player in rolls.keys()}
    for player, player_rolls in rolls.items():
        for roll in player_rolls:
            positions[player] = (positions[player] + roll) % board_positions
    return positions