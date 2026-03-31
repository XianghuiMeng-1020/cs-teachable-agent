def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or not all(isinstance(x, int) and x >= 0 for x in board_state):
        return 0
    if not (1 <= roll <= 6):
        return 0

    max_index = len(board_state) - 1
    destination_index = min(roll, max_index)
    tokens_collected = sum(board_state[:destination_index + 1])

    for i in range(destination_index + 1):
        board_state[i] = 0

    return tokens_collected