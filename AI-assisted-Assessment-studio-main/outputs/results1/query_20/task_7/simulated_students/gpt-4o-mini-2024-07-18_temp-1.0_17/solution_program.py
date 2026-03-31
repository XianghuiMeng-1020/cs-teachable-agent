def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    # Convert the profit/loss string into a list of integers
    board_profit = list(map(int, board_profit.split()))
    n = len(board_profit)  # Total number of squares on the board

    # Calculate the new position on the circular board
    new_position = (current_position - 1 + dice_roll) % n + 1
    # Update the net money based on the profit/loss from the new position
    updated_money = net_money + board_profit[new_position - 1]

    return (new_position, updated_money)