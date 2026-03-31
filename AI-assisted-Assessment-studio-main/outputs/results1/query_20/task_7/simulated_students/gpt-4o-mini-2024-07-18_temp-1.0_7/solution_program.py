def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    board_profit_list = list(map(int, board_profit.split()))
    board_size = len(board_profit_list)
    new_position = (current_position + dice_roll - 1) % board_size + 1
    updated_money = net_money + board_profit_list[new_position - 1]
    return (new_position, updated_money)