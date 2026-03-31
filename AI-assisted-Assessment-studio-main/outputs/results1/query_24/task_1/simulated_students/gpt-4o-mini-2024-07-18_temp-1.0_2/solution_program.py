def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or not all(isinstance(x, int) and x >= 0 for x in board_state):
        return 0
    if not (1 <= roll <= 6):
        return 0
    total_tokens = 0
    end_position = min(len(board_state), roll)
    for i in range(end_position):
        total_tokens += board_state[i]
        board_state[i] = 0
    if roll > len(board_state):
        roll = len(board_state)
    return total_tokens