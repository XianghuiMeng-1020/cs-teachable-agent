def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or not all(isinstance(x, int) and x >= 0 for x in board_state):
        return 0
    if not (1 <= roll <= 6):
        return 0
    
    start = 0
    destination = min(len(board_state) - 1, start + roll)
    tokens_collected = sum(board_state[start:destination + 1])
    
    for i in range(start, destination + 1):
        board_state[i] = 0
    
    return tokens_collected