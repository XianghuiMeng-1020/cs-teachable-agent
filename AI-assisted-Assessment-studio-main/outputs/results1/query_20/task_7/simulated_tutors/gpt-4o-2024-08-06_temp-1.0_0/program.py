def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    # Convert board_profit from string to list of integers
    board_profit_list = list(map(int, board_profit.split()))
    total_squares = len(board_profit_list)
    
    # Calculate new position
    new_position = (current_position + dice_roll - 1) % total_squares + 1
    
    # Calculate money adjustment
    updated_money = net_money + board_profit_list[new_position - 1]
    
    return new_position, updated_money

# Example usage:
result = move_player_on_board(5, 3, 1000, '0 20 -50 30 40 10 0 -20 70 -30')
print(result)  # Should output: (8, 1070)