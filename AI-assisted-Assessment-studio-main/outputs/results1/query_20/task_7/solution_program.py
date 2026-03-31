def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    profits = board_profit.split()
    n = len(profits)
    new_position = (current_position - 1 + dice_roll) % n + 1
    updated_money = net_money + int(profits[new_position - 1])
    return new_position, updated_money
