def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or not all(isinstance(x, int) and x >= 0 for x in board_state):
        return 0
    if not (1 <= roll <= 6):
        return 0
    
    total_tokens = 0
    current_position = 0
    destination_position = min(current_position + roll, len(board_state) - 1)
    
    for i in range(current_position, destination_position + 1):
        total_tokens += board_state[i]
        board_state[i] = 0
    
    return total_tokens