def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or any(
        not isinstance(x, int) or x < 0 for x in board_state
    ):
        return 0
    
    if not (1 <= roll <= 6):
        return 0
    
    total_tokens = 0
    length = len(board_state)
    destination = min(roll, length)
    
    for i in range(destination):
        total_tokens += board_state[i]
        board_state[i] = 0
    
    return total_tokens