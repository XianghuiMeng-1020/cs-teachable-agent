def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    board_profit_list = list(map(int, board_profit.split()))
    number_of_squares = len(board_profit_list)
    new_position = (current_position - 1 + dice_roll) % number_of_squares
    new_position += 1  # Convert 0-based index back to 1-based index
    updated_money = net_money + board_profit_list[new_position - 1]  # Adjusting for 1-based index
    return (new_position, updated_money)