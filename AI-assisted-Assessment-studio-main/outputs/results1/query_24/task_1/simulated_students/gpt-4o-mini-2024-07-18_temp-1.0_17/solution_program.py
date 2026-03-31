def simulate_turn(board_state, roll):
    if not isinstance(board_state, list) or any(not isinstance(x, int) or x < 0 for x in board_state):
        return 0
    if not (1 <= roll <= 6):
        return 0
    total_tokens = 0
    max_index = len(board_state) - 1
    destination_index = min(roll, max_index)
    total_tokens = sum(board_state[0:destination_index + 1])
    for i in range(0, destination_index + 1):
        board_state[i] = 0
    return total_tokens