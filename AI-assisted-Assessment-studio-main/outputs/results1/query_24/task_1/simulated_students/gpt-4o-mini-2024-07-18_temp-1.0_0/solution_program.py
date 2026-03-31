def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or not all(isinstance(i, int) and i >= 0 for i in board_state):
        return 0
    if not (1 <= roll <= 6):
        return 0
    total_tokens = 0
    board_length = len(board_state)
    destination = min(roll, board_length)
    for i in range(destination):
        total_tokens += board_state[i]
        board_state[i] = 0
    return total_tokens