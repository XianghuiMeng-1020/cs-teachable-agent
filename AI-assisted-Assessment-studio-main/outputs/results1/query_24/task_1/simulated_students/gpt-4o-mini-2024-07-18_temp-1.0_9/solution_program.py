def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or not all(isinstance(x, int) and x >= 0 for x in board_state) or 
       not isinstance(roll, int) or roll < 1 or roll > 6:
        return 0

    total_tokens = 0
    player_position = 0
    move_to_position = min(len(board_state) - 1, player_position + roll)

    for i in range(player_position, move_to_position + 1):
        total_tokens += board_state[i]
        board_state[i] = 0

    return total_tokens