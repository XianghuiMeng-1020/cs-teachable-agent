def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    board_profit_list = list(map(int, board_profit.split()))
    num_squares = len(board_profit_list)
    new_position = (current_position + dice_roll - 1) % num_squares
    new_position = new_position + 1  # converting to 1-based index
    updated_money = net_money + board_profit_list[new_position - 1]
    return (new_position, updated_money)