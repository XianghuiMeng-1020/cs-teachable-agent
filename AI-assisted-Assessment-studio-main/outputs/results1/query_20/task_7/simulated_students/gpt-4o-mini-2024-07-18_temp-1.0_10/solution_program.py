def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    board_profit_list = list(map(int, board_profit.split()))
    n = len(board_profit_list)
    new_position = (current_position + dice_roll - 1) % n
    if new_position == 0:
        new_position = n
    new_money = net_money + board_profit_list[new_position - 1]
    return (new_position, new_money)