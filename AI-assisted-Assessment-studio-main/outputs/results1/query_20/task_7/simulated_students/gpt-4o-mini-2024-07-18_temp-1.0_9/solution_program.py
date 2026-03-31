def move_player_on_board(current_position, dice_roll, net_money, board_profit):
    # Convert board_profit string to a list of integers
    profits = list(map(int, board_profit.split()))
    n = len(profits)  # Number of squares on the board

    # Calculate new position (1-based index)
    new_position = (current_position - 1 + dice_roll) % n + 1
    # Adjust net money based on the profit/loss of the landed square
    updated_money = net_money + profits[new_position - 1]  # new_position is 1-based

    return (new_position, updated_money)