def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or 
       not all(isinstance(x, int) and x >= 0 for x in board_state) or 
       not (1 <= roll <= 6):
        return 0
    
    start_index = 0
    end_index = min(start_index + roll, len(board_state))
    tokens_collected = sum(board_state[start_index:end_index])
    
    for i in range(start_index, end_index):
        board_state[i] = 0
    
    return tokens_collected