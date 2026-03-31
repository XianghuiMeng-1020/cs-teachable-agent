def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or not all(isinstance(x, int) and x >= 0 for x in board_state):
        return 0
    if not (1 <= roll <= 6):
        return 0
    
    position = min(roll, len(board_state))
    tokens_collected = sum(board_state[0:position])
    for i in range(position):
        board_state[i] = 0
    
    return tokens_collected