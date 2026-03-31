def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or 
       not all(isinstance(x, int) and x >= 0 for x in board_state) or 
       not (1 <= roll <= 6):
        return 0
    
    start = 0
    end = min(start + roll, len(board_state))
    total_tokens = sum(board_state[start:end])
    for i in range(start, end):
        board_state[i] = 0
    
    return total_tokens