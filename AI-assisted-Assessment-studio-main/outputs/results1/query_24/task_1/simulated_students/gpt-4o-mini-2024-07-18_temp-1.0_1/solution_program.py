def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or not all(isinstance(x, int) and x >= 0 for x in board_state) or not (1 <= roll <= 6):
        return 0
    
    total_tokens = 0
    n = len(board_state)
    final_position = min(roll, n)  # Don't exceed the board length

    for i in range(final_position):
        total_tokens += board_state[i]
        board_state[i] = 0  # Deduct tokens to zero
    
    return total_tokens