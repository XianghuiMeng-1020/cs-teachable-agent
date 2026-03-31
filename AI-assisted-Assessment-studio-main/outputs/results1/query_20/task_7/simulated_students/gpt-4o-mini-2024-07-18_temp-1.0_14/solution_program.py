def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    board_profit_list = list(map(int, board_profit.split()))
    total_squares = len(board_profit_list)
    new_position = (current_position - 1 + dice_roll) % total_squares
    new_position = new_position + 1  # Convert to 1-based index
    updated_money = net_money + board_profit_list[new_position - 1]  # Adjust for 1-based index
    return (new_position, updated_money)