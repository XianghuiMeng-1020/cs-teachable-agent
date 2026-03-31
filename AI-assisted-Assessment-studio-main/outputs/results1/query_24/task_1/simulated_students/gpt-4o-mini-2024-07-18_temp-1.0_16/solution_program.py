def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or not all(isinstance(x, int) and x >= 0 for x in board_state):
        return 0
    if not isinstance(roll, int) or roll < 1 or roll > 6:
        return 0
    tokens_collected = 0
    last_slot = min(roll, len(board_state))
    for i in range(last_slot):
        tokens_collected += board_state[i]
        board_state[i] = 0
    return tokens_collected