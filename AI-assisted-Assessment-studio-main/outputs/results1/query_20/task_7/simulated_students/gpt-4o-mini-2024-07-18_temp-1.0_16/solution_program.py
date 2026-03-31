def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    # Split and convert the board_profit string into a list of integers
    profits = list(map(int, board_profit.split()))
    board_size = len(profits)  # total number of squares on the board
    
    # Calculate the new position using modulo for circular movement
    new_position = (current_position + dice_roll - 1) % board_size  # -1 for 0-based index
    if new_position == 0:
        new_position = board_size  # fix to 1-based index
    
    # Update money based on the profit/loss of the landed square
    updated_money = net_money + profits[new_position - 1]  # -1 for 0-based access
    
    return (new_position, updated_money)