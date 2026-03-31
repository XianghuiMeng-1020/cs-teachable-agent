def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    board_profit = list(map(int, board_profit.split()))
    n = len(board_profit)
    new_position = (current_position + dice_roll - 1) % n + 1
    updated_money = net_money + board_profit[new_position - 1]
    return (new_position, updated_money)