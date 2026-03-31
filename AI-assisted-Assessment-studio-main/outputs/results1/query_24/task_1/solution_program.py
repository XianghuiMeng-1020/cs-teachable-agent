def simulate_turn(board_state, roll):
    try:
        if not isinstance(board_state, list) or not all(isinstance(x, int) and x >= 0 for x in board_state):
            return 0
        if not isinstance(roll, int) or roll < 1 or roll > 6:
            return 0
        total_tokens = 0
        for i in range(min(roll, len(board_state))):
            total_tokens += board_state[i]
            board_state[i] = 0
        return total_tokens
    except Exception:
        return 0
