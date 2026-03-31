def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    board_profit_list = list(map(int, board_profit.split()))
    n = len(board_profit_list)
    new_position = (current_position - 1 + dice_roll) % n
    updated_money = net_money + board_profit_list[new_position]
    return (new_position + 1, updated_money)