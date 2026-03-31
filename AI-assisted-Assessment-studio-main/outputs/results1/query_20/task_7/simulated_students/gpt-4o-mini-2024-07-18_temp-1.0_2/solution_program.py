def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    # Convert the board_profit string to a list of integers
    profits = list(map(int, board_profit.split()))
    num_squares = len(profits)
    # Calculate the new position on the board (1-based index)
    new_position = (current_position - 1 + dice_roll) % num_squares + 1
    # Update the money based on the profit/loss at the new position
    updated_money = net_money + profits[new_position - 1]
    return (new_position, updated_money)