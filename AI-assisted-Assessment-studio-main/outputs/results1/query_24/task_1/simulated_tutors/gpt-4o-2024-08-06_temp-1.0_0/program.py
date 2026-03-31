def simulate_turn(board_state, roll):
    # Exception handling for invalid inputs
    try:
        if not (isinstance(board_state, list) and all(isinstance(x, int) and x >= 0 for x in board_state)):
            return 0
        if not isinstance(roll, int) or roll < 1 or roll > 6:
            return 0
        
        # Variables
        collected_tokens = 0
        max_idx = min(len(board_state) - 1, roll)

        # Loops
        for i in range(max_idx + 1):
            collected_tokens += board_state[i]
            board_state[i] = 0

        return collected_tokens

    except Exception as e:
        # Handle unexpected exceptions
        return 0